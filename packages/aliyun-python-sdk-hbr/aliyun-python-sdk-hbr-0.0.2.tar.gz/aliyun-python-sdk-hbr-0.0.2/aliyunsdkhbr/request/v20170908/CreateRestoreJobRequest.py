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

class CreateRestoreJobRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'hbr', '2017-09-08', 'CreateRestoreJob','hbr')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_TargetPrefix(self):
		return self.get_query_params().get('TargetPrefix')

	def set_TargetPrefix(self,TargetPrefix):
		self.add_query_param('TargetPrefix',TargetPrefix)

	def get_SnapshotId(self):
		return self.get_query_params().get('SnapshotId')

	def set_SnapshotId(self,SnapshotId):
		self.add_query_param('SnapshotId',SnapshotId)

	def get_TargetCreateTime(self):
		return self.get_query_params().get('TargetCreateTime')

	def set_TargetCreateTime(self,TargetCreateTime):
		self.add_query_param('TargetCreateTime',TargetCreateTime)

	def get_VaultId(self):
		return self.get_query_params().get('VaultId')

	def set_VaultId(self,VaultId):
		self.add_query_param('VaultId',VaultId)

	def get_SnapshotHash(self):
		return self.get_query_params().get('SnapshotHash')

	def set_SnapshotHash(self,SnapshotHash):
		self.add_query_param('SnapshotHash',SnapshotHash)

	def get_TargetClientId(self):
		return self.get_body_params().get('TargetClientId')

	def set_TargetClientId(self,TargetClientId):
		self.add_body_params('TargetClientId', TargetClientId)

	def get_Options(self):
		return self.get_query_params().get('Options')

	def set_Options(self,Options):
		self.add_query_param('Options',Options)

	def get_SourceType(self):
		return self.get_query_params().get('SourceType')

	def set_SourceType(self,SourceType):
		self.add_query_param('SourceType',SourceType)

	def get_TargetBucket(self):
		return self.get_query_params().get('TargetBucket')

	def set_TargetBucket(self,TargetBucket):
		self.add_query_param('TargetBucket',TargetBucket)

	def get_UdmDetail(self):
		return self.get_query_params().get('UdmDetail')

	def set_UdmDetail(self,UdmDetail):
		self.add_query_param('UdmDetail',UdmDetail)

	def get_RestoreType(self):
		return self.get_query_params().get('RestoreType')

	def set_RestoreType(self,RestoreType):
		self.add_query_param('RestoreType',RestoreType)

	def get_TargetInstanceId(self):
		return self.get_body_params().get('TargetInstanceId')

	def set_TargetInstanceId(self,TargetInstanceId):
		self.add_body_params('TargetInstanceId', TargetInstanceId)

	def get_TargetFileSystemId(self):
		return self.get_query_params().get('TargetFileSystemId')

	def set_TargetFileSystemId(self,TargetFileSystemId):
		self.add_query_param('TargetFileSystemId',TargetFileSystemId)

	def get_TargetPath(self):
		return self.get_body_params().get('TargetPath')

	def set_TargetPath(self,TargetPath):
		self.add_body_params('TargetPath', TargetPath)

	def get_UdmRegionId(self):
		return self.get_query_params().get('UdmRegionId')

	def set_UdmRegionId(self,UdmRegionId):
		self.add_query_param('UdmRegionId',UdmRegionId)