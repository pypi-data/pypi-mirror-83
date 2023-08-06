from localstack.utils.aws import aws_models
jmiIh=super
jmiIB=None
jmiIb=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  jmiIh(LambdaLayer,self).__init__(arn)
  self.cwd=jmiIB
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.jmiIb.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,jmiIb,env=jmiIB):
  jmiIh(RDSDatabase,self).__init__(jmiIb,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,jmiIb,env=jmiIB):
  jmiIh(RDSCluster,self).__init__(jmiIb,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,jmiIb,env=jmiIB):
  jmiIh(AppSyncAPI,self).__init__(jmiIb,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,jmiIb,env=jmiIB):
  jmiIh(AmplifyApp,self).__init__(jmiIb,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,jmiIb,env=jmiIB):
  jmiIh(ElastiCacheCluster,self).__init__(jmiIb,env=env)
class TransferServer(BaseComponent):
 def __init__(self,jmiIb,env=jmiIB):
  jmiIh(TransferServer,self).__init__(jmiIb,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,jmiIb,env=jmiIB):
  jmiIh(CloudFrontDistribution,self).__init__(jmiIb,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,jmiIb,env=jmiIB):
  jmiIh(CodeCommitRepository,self).__init__(jmiIb,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
