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
from aliyunsdksmartag.endpoint import endpoint_data

class UnicomSignConfirmRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Smartag', '2018-03-13', 'UnicomSignConfirm','smartag')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_ResourceOwnerId(self):
		return self.get_query_params().get('ResourceOwnerId')

	def set_ResourceOwnerId(self,ResourceOwnerId):
		self.add_query_param('ResourceOwnerId',ResourceOwnerId)

	def get_ResourceOwnerAccount(self):
		return self.get_query_params().get('ResourceOwnerAccount')

	def set_ResourceOwnerAccount(self,ResourceOwnerAccount):
		self.add_query_param('ResourceOwnerAccount',ResourceOwnerAccount)

	def get_OwnerAccount(self):
		return self.get_query_params().get('OwnerAccount')

	def set_OwnerAccount(self,OwnerAccount):
		self.add_query_param('OwnerAccount',OwnerAccount)

	def get_TmsOrders(self):
		return self.get_query_params().get('TmsOrder')

	def set_TmsOrders(self, TmsOrders):
		for depth1 in range(len(TmsOrders)):
			if TmsOrders[depth1].get('TmsCode') is not None:
				self.add_query_param('TmsOrder.' + str(depth1 + 1) + '.TmsCode', TmsOrders[depth1].get('TmsCode'))
			if TmsOrders[depth1].get('SigningTime') is not None:
				self.add_query_param('TmsOrder.' + str(depth1 + 1) + '.SigningTime', TmsOrders[depth1].get('SigningTime'))
			if TmsOrders[depth1].get('TmsOrderCode') is not None:
				self.add_query_param('TmsOrder.' + str(depth1 + 1) + '.TmsOrderCode', TmsOrders[depth1].get('TmsOrderCode'))
			if TmsOrders[depth1].get('TradeId') is not None:
				self.add_query_param('TmsOrder.' + str(depth1 + 1) + '.TradeId', TmsOrders[depth1].get('TradeId'))

	def get_OwnerId(self):
		return self.get_query_params().get('OwnerId')

	def set_OwnerId(self,OwnerId):
		self.add_query_param('OwnerId',OwnerId)