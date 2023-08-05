from localstack.utils.aws import aws_models
UbzrT=super
UbzrX=None
Ubzrt=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  UbzrT(LambdaLayer,self).__init__(arn)
  self.cwd=UbzrX
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.Ubzrt.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,Ubzrt,env=UbzrX):
  UbzrT(RDSDatabase,self).__init__(Ubzrt,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,Ubzrt,env=UbzrX):
  UbzrT(RDSCluster,self).__init__(Ubzrt,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,Ubzrt,env=UbzrX):
  UbzrT(AppSyncAPI,self).__init__(Ubzrt,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,Ubzrt,env=UbzrX):
  UbzrT(AmplifyApp,self).__init__(Ubzrt,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,Ubzrt,env=UbzrX):
  UbzrT(ElastiCacheCluster,self).__init__(Ubzrt,env=env)
class TransferServer(BaseComponent):
 def __init__(self,Ubzrt,env=UbzrX):
  UbzrT(TransferServer,self).__init__(Ubzrt,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,Ubzrt,env=UbzrX):
  UbzrT(CloudFrontDistribution,self).__init__(Ubzrt,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,Ubzrt,env=UbzrX):
  UbzrT(CodeCommitRepository,self).__init__(Ubzrt,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
