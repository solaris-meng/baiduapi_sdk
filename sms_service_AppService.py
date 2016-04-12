#coding=utf-8
from ApiSDKJsonClient import *


class sms_service_AppService(ApiSDKJsonClient):

	def __init__(self):
		ApiSDKJsonClient.__init__(self, 'sms', 'service', 'AppService')

	def submitAppStatus(self, submitAppStatusRequest=None):
		return self.execute('submitAppStatus', submitAppStatusRequest)



