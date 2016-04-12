#coding=utf-8
import traceback as tb
import random
import string
import requests
import hashlib

from ApiSDKJsonClient import *
from sms_service_AccountService import *
from sms_service_CampaignService import *
from sms_service_AdgroupService import *
from sms_service_ReportService import *

start_date = "2016-03-28 12:00:00"
end_date = "2016-03-29 12:00:00"
url = 'http://101.200.130.178:7000/baidusys/DanyuanDailyReport/'

#############################################
###### 策略炒股通
USER = 'Baidu-无线bc-智投智道2160884'
PWD = 'QAZqaz123'
TOKEN ='3b759c3dc320b190b9e7f5571168a5f5'
appid='d7ee59895bf8479d85fefbcd64244c05'
###### 一点资讯
USER = 'Baidu-无线bc-智投智道b2160884'
PWD = 'QAZqaz123'
TOKEN ='c3f1fb39a3a7eee9594355e9a0c99325'
appid='c98ad064a0fa4eab8fba31541de32f59'
#############################################

def set_auth(service):
    service.setUsername(USER)
    service.setPassword(PWD)
    service.setToken(TOKEN)
    return

if __name__ == "__main__":
    try:
        request = {}

        service = sms_service_ReportService()
        set_auth(service)
        res=service.getRealTimeData({"realTimeRequestType":{"performanceData":["impression","click","cost","cpc","ctr","cpm","conversion"],"levelOfDetails":11,"startDate":start_date,"endDate": end_date,"unitOfTime":5,"reportType":14, }})

        for i in res:
            print i

        # get all danyuans
        for i in res["body"]["data"]:
            date = i['date']
            rid = i['id']

            account_name = i["name"][0]
            jihua_name = i["name"][1]
            danyuan_name = i["name"][2]

            kpi_impression = i["kpis"][0]
            kpi_click = i["kpis"][1]
            kpi_cost = i["kpis"][2]
            kpi_cpc = i["kpis"][3]
            kpi_ctr = i["kpis"][4]
            kpi_cpm = i["kpis"][5]
            kpi_conversion = i["kpis"][6]

            #uuid = '%s-%s-%s' % (appid, date, rid)
            uuid_str = '%s-%s-%s-%s' % (date, jihua_name, danyuan_name, appid)
            uuid = hashlib.sha1(uuid_str.encode('utf-8')).hexdigest()

            data = {}
            data['date'] = date
            data['appid'] = appid
            data['rid'] = rid
            data['uuid'] = uuid
            data['account_name'] = account_name
            data['jihua_name'] = jihua_name
            data['danyuan_name'] = danyuan_name
            data['kpi_impression'] = kpi_impression
            data['kpi_click'] = kpi_click
            data['kpi_cost'] = kpi_cost
            data['kpi_cpc'] = kpi_cpc
            data['kpi_cpm'] = kpi_cpm
            data['kpi_ctr'] = kpi_ctr
            data['kpi_conversation'] = kpi_conversion

            #r = requests.post(url, auth=('admin', 'brotec'), json=data)
            #print r.status_code
            #print uuid_str
            #print data
        
    except Exception, e:
        tb.print_exc()

