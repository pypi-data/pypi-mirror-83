from localstack.utils.aws import aws_models
tvxSp=super
tvxSr=None
tvxSc=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  tvxSp(LambdaLayer,self).__init__(arn)
  self.cwd=tvxSr
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.tvxSc.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,tvxSc,env=tvxSr):
  tvxSp(RDSDatabase,self).__init__(tvxSc,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,tvxSc,env=tvxSr):
  tvxSp(RDSCluster,self).__init__(tvxSc,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,tvxSc,env=tvxSr):
  tvxSp(AppSyncAPI,self).__init__(tvxSc,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,tvxSc,env=tvxSr):
  tvxSp(AmplifyApp,self).__init__(tvxSc,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,tvxSc,env=tvxSr):
  tvxSp(ElastiCacheCluster,self).__init__(tvxSc,env=env)
class TransferServer(BaseComponent):
 def __init__(self,tvxSc,env=tvxSr):
  tvxSp(TransferServer,self).__init__(tvxSc,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,tvxSc,env=tvxSr):
  tvxSp(CloudFrontDistribution,self).__init__(tvxSc,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,tvxSc,env=tvxSr):
  tvxSp(CodeCommitRepository,self).__init__(tvxSc,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
