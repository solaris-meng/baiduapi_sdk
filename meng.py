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

USER = 'baidu-无线bc-智道未来o2153173'
PWD = 'ASDasd1234'
TOKEN ='90eef519f7f6279321525939eb5439ee'

def set_auth(service):
    service.setUsername(USER)
    service.setPassword(PWD)
    service.setToken(TOKEN)
    return

if __name__ == "__main__":
    try:
        request = {}

        # account
        '''
        service=sms_service_AccountService()
        service.setUsername(USER)
        service.setPassword(PWD)
        service.setToken(TOKEN)
        request = {"accountFields":["userId", "cost", "regDomain"]}
        res = service.getAccountInfo(request)
        '''

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

        service = sms_service_ReportService()
        set_auth(service)
        #res=service.getRealTimeData({"realTimeRequestType":{"performanceData":["impression","click","cost","cpc","ctr","cpm","conversion"],"levelOfDetails":2,"startDate":"2016-03-13 12:00:00","endDate":"2016-03-15 12:00:00","unitOfTime":1,"reportType":2}})
        res=service.getRealTimeData({"realTimeRequestType":{"performanceData":["impression","click","cost","cpc","ctr","cpm","conversion"],"levelOfDetails":5,"startDate":"2016-03-13 12:00:00","endDate":"2016-03-15 12:00:00","unitOfTime":5,"reportType":11}})
        for i in res["body"]["data"]:
            pass
            print "date:",i["date"]
            print "kpi:",i["kpis"]
            print "id:",i["id"]
            print "name:",i["name"]

        url = 'http://101.200.130.178:7000/baidusys/DanyuanDailyReport/'
        data = {}
        data['date'] = '2016-3-20'
        data['appid'] = 'test'
        data['rid'] = 1
        data['uuid'] = 'appid-date-rid'
        data['account_name'] = 'test'
        data['jihua_name'] = 'test'
        data['danyuan_name'] = 'test'
        data['kpi_impression'] = 1
        data['kpi_click'] =  1236
        data['kpi_cost'] = 1
        data['kpi_cpc'] = 2
        data['kpi_cpm'] = 3
        data['kpi_ctr'] = 3
        data['kpi_conversation'] = 1
        r = requests.post(url, auth=('admin', 'brotec'), json=data)

        
    except Exception, e:
        tb.print_exc()

