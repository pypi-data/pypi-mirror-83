import os
import yaml
import logging
from aws_cdk import (
    aws_codebuild as cb,
    aws_codepipeline as cp,
    aws_codepipeline_actions as cpa,
    aws_codecommit as cc,
    aws_codestarconnections as csc,
    pipelines as cdkpipeline,
    aws_s3 as s3,
    core
)

CONN = os.environ.get('arn:aws:codestar-connections:eu-west-1:605901617242:connection/675a0f98-dd7c-4d72-86c8-57378c507e5d')



class Pipelines(core.Construct):
    artifacts = {
        'sources': [],
        'builds': [],
        'build_extras': [],
        'deploy': []
    }
    actions = {
        'sources': [],
        'builds': [],
        'build_extras': [],
        'deploy': []
    }

    def __init__(self, scope, id, github_config: dict, project_config: dict):
        super().__init__(scope, id)
        self.bucket = s3.Bucket(self, 'bucket',
            removal_policy=core.RemovalPolicy.RETAIN,
            encryption=s3.BucketEncryption.KMS_MANAGED,
            versioned=True
        )
        self.pipe = cp.Pipeline(self, 'pipe', cross_account_keys=True, pipeline_name=id + 'Pipe')

        self._source(**github_config)
        self._project(**project_config)
        self._build(self.artifacts['sources'][0], self.artifacts['build_extras'])
        # self._deploy()

    def _project(self, **project_config):
        if 'build_spec' in project_config:
            project_config['build_spec'] = Pipelines.load_buildspec(project_config['build_spec'])
        self.project = cb.PipelineProject(
            self, "project",
            project_name="{}".format(self.node.id),
            environment=cb.LinuxBuildImage.STANDARD_4_0,
            cache=cb.Cache.bucket(bucket=self.bucket, prefix='codebuild-cache'),
            **project_config
        )

    def _source(self, **github_config):
        artifact = cp.Artifact()

        conn =csc.CfnConnection(
            self, 'ghconn',
            connection_name='{}'.format(github_config['owner']),
            host_arn=CONN,
            #'{}/{}'.format(github_config['owner'], github_config['repo']),
            provider_type='GitHub'
        )
        # cc.Repository(
        #     self, 'ghrepo',
        #     repository_name=github_config['repo']
        # )
        # cpa.CodeCommitSourceAction(
        #     self, 'ccaction',
        #     output=artifact,
        #     repository=
        # )

        checkout = cpa.GitHubSourceAction(
            action_name="{}@{}".format(github_config['repo'], github_config['branch']),
            output=artifact,
            trigger=cpa.GitHubTrigger.POLL,
            **github_config
        )
        self.artifacts['sources'].append(artifact)
        self.actions['sources'].append(checkout)
        self.pipe.add_stage(stage_name='Source@{}'.format(github_config['repo']), actions=[checkout])

    def _build(self, input, extra_inputs=[]):
        artifact = cp.Artifact()
        build = cpa.CodeBuildAction(
            outputs=[artifact],
            type=cpa.CodeBuildActionType.BUILD,
            action_name="Build",
            input=input,
            extra_inputs=extra_inputs,
            project=self.project
        )
        self.artifacts['builds'].append(artifact)
        self.actions['builds'].append(build)

        self.pipe.add_stage(
            stage_name="Build",
            actions=self.actions['builds']
        )

    def _deploy(self, **deploy_config):
        deploy = cpa.CloudFormationCreateUpdateStackAction(
            action_name='Deploy',
            stack_name='iam-idp',
            admin_permissions=True,
            template_path=self.artifacts['builds'][0].at_path("cdk.out/iam-idp.template.json"),
            **deploy_config
        )
        self.actions['deploy'].append(deploy)

    @staticmethod
    def env(environment_variables: dict):
        envs = dict()
        for env, value in environment_variables.items():
            envs[env] = cb.BuildEnvironmentVariable(value=value)
        return envs
    
    @staticmethod
    def load_buildspec(specfile):
        with open(specfile, encoding="utf8") as fp:
            bsfile = fp.read()
            bs = yaml.safe_load(bsfile)
            return cb.BuildSpec.from_object(value=bs)
