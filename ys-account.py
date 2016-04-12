#coding=utf-8
import traceback as tb
import random
import string
import requests

from ApiSDKJsonClient import *
from sms_service_AccountService import *
from sms_service_CampaignService import *
from sms_service_AdgroupService import *
from sms_service_ReportService import *

USER = '北京凌众时代广告'
PWD = 'QAZqaz1235'
TOKEN ='0046d81d8117eb7cf212f5efcf0ae97d'

def set_auth(service):
    service.setUsername(USER)
    service.setPassword(PWD)
    service.setToken(TOKEN)
    return

if __name__ == "__main__":
    try:
        request = {}

        # account
        service=sms_service_AccountService()
        set_auth(service)

        request = {"accountFields":["userId", "cost", "regDomain"]}
        service.getAccountInfo(request)

        #for i in res['body']['data']:
        #    print(i)

        '''
        service=sms_service_CampaignService()
        request = {"campaignIds":[],"campaignFields": ["campaignName"],}
        set_auth(service)
        res = service.getCampaign(request)
        body = res['body']
        for i in body['data']:
            #print 'Jihua:',i['campaignName']
            #print 'Jihua id:', i['campaignId']

            # get danyuans per jihua
            service=sms_service_AdgroupService()
            set_auth(service)
            ids = []
            ids.append(i['campaignId'])
            request = {"ids":ids, "idType": 3, "adgroupFields":["adgroupId","adgroupName","campaignId",]}
            res = service.getAdgroup(request)
            bd_dy = res['body']
            for j in bd_dy['data']:
                print 'Danyuan id:', j['adgroupId']
                print 'Jihua id:', j['campaignId']
                print 'Jihua name:', j['adgroupName']
        '''

    except Exception, e:
        tb.print_exc()

