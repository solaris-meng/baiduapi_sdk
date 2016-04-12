#coding=utf-8
import traceback as tb
import random
import string
import requests
import xlwt
import sys

from ApiSDKJsonClient import *
from sms_service_AccountService import *
from sms_service_CampaignService import *
from sms_service_AdgroupService import *
from sms_service_ReportService import *
from sms_service_KeywordService import *

'''
#Test account
USER = 'baidu-无线bc-智道未来o2153173'
PWD = 'ASDasd1234'
TOKEN ='90eef519f7f6279321525939eb5439ee'
'''

# 一点资讯
USER = 'Baidu-无线bc-智投智道b2160884'
PWD = 'QAZqaz123'
TOKEN ='c3f1fb39a3a7eee9594355e9a0c99325'

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
        service.setUsername(USER)
        service.setPassword(PWD)
        service.setToken(TOKEN)
        request = {"accountFields":["userId", "cost", "regDomain"]}
        res = service.getAccountInfo(request)
        print res
        sys.exit()

        wb = xlwt.Workbook()
        ws = wb.add_sheet('word sheet')
        font0 = xlwt.Font()
        font0.name = 'Times New Roman'
        font0.colour_index = 2
        font0.bold = False
  
        style0 = xlwt.XFStyle()
        style0.font = font0

        row0 = [u'计划名',u'计划ID',u'单元名',u'单元ID',u'关键词',u'关键词ID']
        for i in range(0,len(row0)):
            ws.write(0,i,row0[i],style0)

        row = 1

        # Jihua -> Danyuan -> Keyword
        service=sms_service_CampaignService()
        req_jh = {"campaignIds":[],"campaignFields": ["campaignName", "campaignId"],}
        set_auth(service)
        res = service.getCampaign(req_jh)
        body = res['body']
        for i in body['data']:
            jihua_id = i['campaignId']
            jihua_name = i['campaignName']

            if jihua_id != 56366383:
                continue

            # get danyuans per jihua
            service=sms_service_AdgroupService()
            set_auth(service)
            ids = []
            ids.append(jihua_id)
            req_dy = {"ids":ids, "idType": 3, "adgroupFields":["adgroupId","adgroupName","campaignId",]}
            res = service.getAdgroup(req_dy)
            bd_dy = res['body']
            for j in bd_dy['data']:
                #print 'Jihua id:', jihua_id
                #print 'Jihua name:', jihua_name
                #print 'Danyuan id:', j['adgroupId']
                #print 'Danyuan name:', j['adgroupName']
                #print(j)
                danyuan_id = j['adgroupId']
                danyuan_name = j['adgroupName']

                service = sms_service_KeywordService()
                set_auth(service)
                ids_dy = []
                ids_dy.append(danyuan_id)
                req_ky = {"wordFields":["keyword", "keywordId"],"idType":5,"ids":ids_dy, "getTemp":0}
                res = service.getWord(req_ky)
                for k in res['body']['data']:
                    word_id = k['keywordId']
                    word_name = k['keyword']

                    #row0 = [u'计划名',u'计划ID',u'单元名',u'单元ID',u'关键词',u'关键词ID']
                    ws.write(row,0, jihua_name,style0)
                    ws.write(row,1, jihua_id,style0)
                    ws.write(row,2, danyuan_name,style0)
                    ws.write(row,3, danyuan_id,style0)
                    ws.write(row,4, word_name,style0)
                    ws.write(row,5, word_id,style0)
                    row = row + 1
        wb.save('words.xls')
    except Exception, e:
        tb.print_exc()

