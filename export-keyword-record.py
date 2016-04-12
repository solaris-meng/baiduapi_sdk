#coding=utf-8
import traceback as tb
import random
import string
import requests
import xlwt

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
start_date = "2016-03-29"
end_date = "2016-03-30"
USER = 'Baidu-无线bc-智投智道b2160884'
PWD = 'QAZqaz123'
TOKEN ='c3f1fb39a3a7eee9594355e9a0c99325'

def set_auth(service):
    service.setUsername(USER)
    service.setPassword(PWD)
    service.setToken(TOKEN)
    return

def get_word_for_jihua(jihuaid, jihuaname):
    try:
        request = {}

        jihuaids = []
        jihuaids.append(jihuaid)
        filename = "keywords-for-jihua-%d-%s.xls" % (jihuaid, jihuaname)

        service = sms_service_ReportService()
        set_auth(service)
        res=service.getRealTimeData({"realTimeRequestType":{"performanceData":["impression","click","cost","cpc","ctr","cpm","conversion"],"levelOfDetails":11,"startDate":start_date,"endDate": end_date,"unitOfTime":5,"reportType":14, "statIds":jihuaids, "statRange":3, "number":5000}})

        ###############################
        wb = xlwt.Workbook()
        ws = wb.add_sheet('word sheet')
        font0 = xlwt.Font()
        font0.name = 'Times New Roman'
        font0.colour_index = 2
        font0.bold = False
  
        style0 = xlwt.XFStyle()
        style0.font = font0

        row0 = [u'帐户名', u'计划名', u'单元名',u'关键词ID',u'关键词',u'impression',u'click',u'cost',u'cpc',u'ctr',u'cpm', u'conversion']
        for i in range(0,len(row0)):
            ws.write(0,i,row0[i],style0)
        row = 1
        ################################

        # Jihua -> Danyuan -> Keyword
        service=sms_service_CampaignService()
        req_jh = {"campaignIds":[],"campaignFields": ["campaignName", "campaignId"],}
        set_auth(service)
        #for i in res:
        #    print i

        # get all danyuans
        for i in res["body"]["data"]:
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

            ws.write(row,0, account_name,style0)
            ws.write(row,1, jihua_name,style0)
            ws.write(row,2, danyuan_name,style0)
            ws.write(row,3, kid,style0)
            ws.write(row,4, keyword_name,style0)

            ws.write(row,5, kpi_impression,style0)
            ws.write(row,6, kpi_click,style0)
            ws.write(row,7, kpi_cost,style0)
            ws.write(row,8, kpi_cpc,style0)
            ws.write(row,9, kpi_ctr,style0)
            ws.write(row,10, kpi_cpm,style0)
            ws.write(row,11, kpi_conversion,style0)

            row = row + 1
            continue
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
        wb.save(filename)
        
    except Exception, e:
        tb.print_exc()

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
        for i in res:
            print i
        body = res['body']
        for i in body['data']:
            jihua_id = i['campaignId']
            jihua_name = i['campaignName']

            get_word_for_jihua(jihua_id, jihua_name)

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

