import os
import logging
from aws_cdk import (
    aws_iam as iam,
    aws_lambda,
    aws_ssm as ssm,
    aws_cloudformation as cfn,
    core
)
from .cdk_lambda import CDKLambda


class IAMIdpSAML(CDKLambda):
    _idp: cfn.CfnCustomResource = None

    def __init__(self,  scope: core.Construct, id: str, idp_name: str, idp_url: str, *, debug=False):
        """Create an IAM SAML Identity Provider

        Args:
            scope (core.Construct): [description]
            id (str): [description]
            idp_name (str): IAM Idp name
            idp_url (str): Your SAML Identity provider URL
        """
        rdir = os.path.dirname(os.path.dirname(__file__))
        lambda_attrs=dict(
                code=aws_lambda.InlineCode(CDKLambda._code_inline(rdir + '/lambdas/iam_idp/saml.py')),
                handler='index.handler',
                timeout=core.Duration.seconds(20),
                runtime=aws_lambda.Runtime.PYTHON_3_7
        )
        # TODO: release layer
        # pip install -r requirements.txt -t .
        layer_path=rdir + '/build/artifacts-cfn_resources.zip'
        layer_attrs=dict(
            description='cfn_resources layer for idp',
            code=aws_lambda.AssetCode(layer_path)
        )
        super().__init__(scope, id, lambda_attrs=lambda_attrs, layer_attrs=layer_attrs, remote_account_grant=False)

        # Add required policies for the lambda to create an IAM idp
        self._lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=['iam:CreateSAMLProvider', 'iam:UpdateSAMLProvider', 'iam:DeleteSAMLProvider'],
                effect=iam.Effect.ALLOW,
                resources=['*']
            )
        )

        self._idp = cfn.CustomResource(
            self, "identityProvider",
            resource_type='Custom::SAMLProvider',
            provider=cfn.CustomResourceProvider.lambda_(self._lambda),
            properties=dict(
                Name=idp_name,
                URL=idp_url
            )
        )
        self.response = self._idp.get_att("Response").to_string()

        # Export
        ssm_name = '/' + id.replace('-', '/')
        ssm.StringParameter(self, 'ssm', string_value=self._idp.ref, parameter_name=ssm_name)
        core.CfnOutput(self, 'IAMIdpSAMLArn', value=self._idp.ref)

    @property
    def arn(self):
        return self._idp.ref

    @property
    def idp(self):
        return self._idp
