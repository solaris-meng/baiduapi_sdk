#coding=utf-8
import traceback
import random
import string
import requests
import hashlib
import xlwt

from ApiSDKJsonClient import *
from sms_service_AccountService import *
from sms_service_CampaignService import *
from sms_service_AdgroupService import *
from sms_service_ReportService import *

#start_date = "2016-04-04"
#end_date = start_date
#end_date = "2016-03-28"
url = 'http://101.200.130.178:7000/baidusys/DanyuanDailyReport/'

#############################################
###### 策略炒股通
#USER = 'Baidu-无线bc-智投智道2160884'
#PWD = 'QAZqaz123'
#TOKEN ='3b759c3dc320b190b9e7f5571168a5f5'
#appid='d7ee59895bf8479d85fefbcd64244c05'
###### 一点资讯
USER = 'Baidu-无线bc-智投智道b2160884'
PWD = 'QAZqaz123'
TOKEN ='c3f1fb39a3a7eee9594355e9a0c99325'
#appid='c98ad064a0fa4eab8fba31541de32f59'
#############################################

def set_auth(service):
    service.setUsername(USER)
    service.setPassword(PWD)
    service.setToken(TOKEN)
    return

def get_account_info():
    try:
        service=sms_service_AccountService()
        set_auth(service)
        request = {"accountFields":["userId", "cost", "regDomain"]}
        res = service.getAccountInfo(request)

        account_id = res['body']['data'][0]['userId']

        rv = {}
        rv['account_name'] = USER
        rv['account_id'] = account_id
        return rv
    except Exception as e:
        err = traceback.format_exc()
        print err
        return 'failed'
#
def get_all_danyuan():
    try:

        all_danyuan = []

        service=sms_service_CampaignService()
        req_jh = {"campaignIds":[],"campaignFields": ["campaignName", "campaignId"],}
        set_auth(service)
        res = service.getCampaign(req_jh)

        for i in res:
            pritn
        # all jihua
        body = res['body']
        for i in body['data']:
            jihua_id = i['campaignId']
            jihua_name = i['campaignName']

            # get danyuans per jihua
            service=sms_service_AdgroupService()
            set_auth(service)
            ids = []
            ids.append(jihua_id)
            req_dy = {"ids":ids, "idType": 3, "adgroupFields":["adgroupId","adgroupName","campaignId",]}

            res = service.getAdgroup(req_dy)
            bd_dy = res['body']
            for j in bd_dy['data']:
                danyuan_id = j['adgroupId']
                danyuan_name = j['adgroupName']

                item={}
                item['jihua_id'] = jihua_id
                item['jihua_name'] = jihua_name
                item['danyuan_id'] = danyuan_id
                item['danyuan_name'] = danyuan_name
                all_danyuan.append(item)
        return all_danyuan
    except Exception as e:
        err = traceback.format_exc()
        print err
        return 'failed'

def get_word_for_jihua_xls(account_id, jihua_id_list, start_date, filename):
    try:
        request = {}



        ###############################
        wb = xlwt.Workbook()
        ws = wb.add_sheet('word sheet')
        font0 = xlwt.Font()
        font0.name = 'Times New Roman'
        font0.colour_index = 0
        font0.bold = False
        font0.height = 320
  
        style0 = xlwt.XFStyle()
        style0.font = font0

        row0 = [u'帐户ID', u'帐户名', u'计划ID', u'计划名', u'单元名',u'关键词ID',u'关键词',u'impression',u'click',u'cost',u'cpc',u'ctr',u'cpm', u'conversion', u'日期']
        for i in range(0,len(row0)):
            ws.write(0,i,row0[i],style0)
        row = 1
        ################################

        for jihua_id in jihua_id_list:
            jihuaids = []
            jihuaids.append(jihua_id)

            service = sms_service_ReportService()
            set_auth(service)
            res=service.getRealTimeData({"realTimeRequestType":{"performanceData":["impression","click","cost","cpc","ctr","cpm","conversion"],"levelOfDetails":11,"startDate":start_date,"endDate": start_date,"unitOfTime":5,"reportType":14, "statIds":jihuaids, "statRange":3, "number":5000}})

            # Jihua -> Danyuan -> Keyword
            service=sms_service_CampaignService()
            req_jh = {"campaignIds":[],"campaignFields": ["campaignName", "campaignId"],}
            set_auth(service)

            # get all danyuans
            for i in res["body"]["data"]:
                print i
                date = i['date']
                kid = i['id']

                account_name = i["name"][0]
                jihua_name = i["name"][1]
                danyuan_name = i["name"][2]
                keyword_name = i["name"][3]

                kpi_impression = i["kpis"][0]
                kpi_click = i["kpis"][1]
                kpi_cost = i["kpis"][2]
                kpi_cpc = i["kpis"][3]
                kpi_ctr = i["kpis"][4]
                kpi_cpm = i["kpis"][5]
                kpi_conversion = i["kpis"][6]

                ws.write(row,0, account_id,style0)
                ws.write(row,1, account_name,style0)
                ws.write(row,2, jihua_id,style0)
                ws.write(row,3, jihua_name,style0)
                ws.write(row,4, danyuan_name,style0)
                ws.write(row,5, kid,style0)
                ws.write(row,6, keyword_name,style0)

                ws.write(row,7, kpi_impression,style0)
                ws.write(row,8, kpi_click,style0)
                ws.write(row,9, kpi_cost,style0)
                ws.write(row,10, kpi_cpc,style0)
                ws.write(row,11, kpi_ctr,style0)
                ws.write(row,12, kpi_cpm,style0)
                ws.write(row,13, kpi_conversion,style0)
                ws.write(row,14, date,style0)

                row = row + 1
                continue

        wb.save(filename)
        return 'success'
        
    except Exception, e:
        err = traceback.print_exc()
        print err
        return 'failed'

# test - cgt - 56246816
#
# yd --- 安卓-驾考-A 56366383
# yd --- 安卓-美食-A 56775408
'''
jihua_id =  56366383
get_word_for_jihua(jihua_id)
jihua_id =  56775408
get_word_for_jihua(jihua_id)
'''

account_info = get_account_info()
account_name = account_info['account_name']
account_id = account_info['account_id']

#danyuans = get_all_danyuan()

#
# for 一点资讯
#
start_date = "2016-04-11"
filename = 'output/一点资讯-%s-安卓-驾考-安卓-美食.xls' % start_date
jihua_id_list = [56366383, 56775408]
rv = get_word_for_jihua_xls(account_id, jihua_id_list, start_date, filename)
print start_date,'---',rv,filename

