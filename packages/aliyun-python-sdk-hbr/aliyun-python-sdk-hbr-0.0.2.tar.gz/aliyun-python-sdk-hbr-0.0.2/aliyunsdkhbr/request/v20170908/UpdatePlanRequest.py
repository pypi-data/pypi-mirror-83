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
from aliyunsdkhbr.endpoint import endpoint_data

class UpdatePlanRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'hbr', '2017-09-08', 'UpdatePlan','hbr')
		self.set_protocol_type('https')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_DiffPolicyId(self):
		return self.get_query_params().get('DiffPolicyId')

	def set_DiffPolicyId(self,DiffPolicyId):
		self.add_query_param('DiffPolicyId',DiffPolicyId)

	def get_ScheduleType(self):
		return self.get_query_params().get('ScheduleType')

	def set_ScheduleType(self,ScheduleType):
		self.add_query_param('ScheduleType',ScheduleType)

	def get_ClientId(self):
		return self.get_query_params().get('ClientId')

	def set_ClientId(self,ClientId):
		self.add_query_param('ClientId',ClientId)

	def get_VaultId(self):
		return self.get_query_params().get('VaultId')

	def set_VaultId(self,VaultId):
		self.add_query_param('VaultId',VaultId)

	def get_IncPolicyId(self):
		return self.get_query_params().get('IncPolicyId')

	def set_IncPolicyId(self,IncPolicyId):
		self.add_query_param('IncPolicyId',IncPolicyId)

	def get_Source(self):
		return self.get_query_params().get('Source')

	def set_Source(self,Source):
		self.add_query_param('Source',Source)

	def get_PlanStatus(self):
		return self.get_query_params().get('PlanStatus')

	def set_PlanStatus(self,PlanStatus):
		self.add_query_param('PlanStatus',PlanStatus)

	def get_PlanName(self):
		return self.get_query_params().get('PlanName')

	def set_PlanName(self,PlanName):
		self.add_query_param('PlanName',PlanName)

	def get_FullPolicyId(self):
		return self.get_query_params().get('FullPolicyId')

	def set_FullPolicyId(self,FullPolicyId):
		self.add_query_param('FullPolicyId',FullPolicyId)

	def get_Retention(self):
		return self.get_query_params().get('Retention')

	def set_Retention(self,Retention):
		self.add_query_param('Retention',Retention)

	def get_Token(self):
		return self.get_query_params().get('Token')

	def set_Token(self,Token):
		self.add_query_param('Token',Token)

	def get_PlanId(self):
		return self.get_query_params().get('PlanId')

	def set_PlanId(self,PlanId):
		self.add_query_param('PlanId',PlanId)