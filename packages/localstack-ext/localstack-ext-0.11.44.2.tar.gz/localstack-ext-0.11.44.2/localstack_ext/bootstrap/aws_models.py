from localstack.utils.aws import aws_models
NaliE=super
NaliB=None
Naliq=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  NaliE(LambdaLayer,self).__init__(arn)
  self.cwd=NaliB
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.Naliq.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,Naliq,env=NaliB):
  NaliE(RDSDatabase,self).__init__(Naliq,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,Naliq,env=NaliB):
  NaliE(RDSCluster,self).__init__(Naliq,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,Naliq,env=NaliB):
  NaliE(AppSyncAPI,self).__init__(Naliq,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,Naliq,env=NaliB):
  NaliE(AmplifyApp,self).__init__(Naliq,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,Naliq,env=NaliB):
  NaliE(ElastiCacheCluster,self).__init__(Naliq,env=env)
class TransferServer(BaseComponent):
 def __init__(self,Naliq,env=NaliB):
  NaliE(TransferServer,self).__init__(Naliq,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,Naliq,env=NaliB):
  NaliE(CloudFrontDistribution,self).__init__(Naliq,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,Naliq,env=NaliB):
  NaliE(CodeCommitRepository,self).__init__(Naliq,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
