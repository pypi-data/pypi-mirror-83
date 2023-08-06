# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
from aliyunsdkdrds.endpoint import endpoint_data

class MyCatCustomImportPreCheckRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Drds', '2019-01-23', 'MyCatCustomImportPreCheck','Drds')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_DstPort(self):
		return self.get_query_params().get('DstPort')

	def set_DstPort(self,DstPort):
		self.add_query_param('DstPort',DstPort)

	def get_TaskName(self):
		return self.get_query_params().get('TaskName')

	def set_TaskName(self,TaskName):
		self.add_query_param('TaskName',TaskName)

	def get_SchemaUrl(self):
		return self.get_query_params().get('SchemaUrl')

	def set_SchemaUrl(self,SchemaUrl):
		self.add_query_param('SchemaUrl',SchemaUrl)

	def get_DstUser(self):
		return self.get_query_params().get('DstUser')

	def set_DstUser(self,DstUser):
		self.add_query_param('DstUser',DstUser)

	def get_DstDbNme(self):
		return self.get_query_params().get('DstDbNme')

	def set_DstDbNme(self,DstDbNme):
		self.add_query_param('DstDbNme',DstDbNme)

	def get_TableMap(self):
		return self.get_query_params().get('TableMap')

	def set_TableMap(self,TableMap):
		self.add_query_param('TableMap',TableMap)

	def get_ImportDb(self):
		return self.get_query_params().get('ImportDb')

	def set_ImportDb(self,ImportDb):
		self.add_query_param('ImportDb',ImportDb)

	def get_DstPwd(self):
		return self.get_query_params().get('DstPwd')

	def set_DstPwd(self,DstPwd):
		self.add_query_param('DstPwd',DstPwd)

	def get_RuleUrl(self):
		return self.get_query_params().get('RuleUrl')

	def set_RuleUrl(self,RuleUrl):
		self.add_query_param('RuleUrl',RuleUrl)

	def get_DstDrdsInstanceId(self):
		return self.get_query_params().get('DstDrdsInstanceId')

	def set_DstDrdsInstanceId(self,DstDrdsInstanceId):
		self.add_query_param('DstDrdsInstanceId',DstDrdsInstanceId)