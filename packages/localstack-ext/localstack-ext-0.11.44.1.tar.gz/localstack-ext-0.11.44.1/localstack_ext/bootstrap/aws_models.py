from localstack.utils.aws import aws_models
bcuwn=super
bcuwK=None
bcuwq=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  bcuwn(LambdaLayer,self).__init__(arn)
  self.cwd=bcuwK
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.bcuwq.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,bcuwq,env=bcuwK):
  bcuwn(RDSDatabase,self).__init__(bcuwq,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,bcuwq,env=bcuwK):
  bcuwn(RDSCluster,self).__init__(bcuwq,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,bcuwq,env=bcuwK):
  bcuwn(AppSyncAPI,self).__init__(bcuwq,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,bcuwq,env=bcuwK):
  bcuwn(AmplifyApp,self).__init__(bcuwq,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,bcuwq,env=bcuwK):
  bcuwn(ElastiCacheCluster,self).__init__(bcuwq,env=env)
class TransferServer(BaseComponent):
 def __init__(self,bcuwq,env=bcuwK):
  bcuwn(TransferServer,self).__init__(bcuwq,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,bcuwq,env=bcuwK):
  bcuwn(CloudFrontDistribution,self).__init__(bcuwq,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,bcuwq,env=bcuwK):
  bcuwn(CodeCommitRepository,self).__init__(bcuwq,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
