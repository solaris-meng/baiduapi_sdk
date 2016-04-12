#coding=utf-8
import traceback as tb
import random
import string
from ApiSDKJsonClient import *
from sms_service_ReportService import *
if __name__ == "__main__":
    try:
        print("###########################test report_service begin.#################################")
        service=sms_service_ReportService()
        
        #getRealTimeQueryData
        #response=service.getRealTimeQueryData({"realTimeQueryRequestType":{"performanceData":["impression","click"],"levelOfDetails":12,"startDate":"2014-03-01 12:00:00","idOnly":"true","endDate":"2015-02-25 12:00:00","unitOfTime":5,"reportType":6}});
        ##print response
        #assert(response["header"]["desc"]=="success" and response["header"]["status"]==0)
        
        #getProfessionalReportId
        response=service.getProfessionalReportId({"reportRequestType":{"performanceData":["impression","click"],"levelOfDetails":12,"startDate":"2014-05-01 12:00:00","endDate":"2015-03-25 12:00:00","unitOfTime":5,"reportType":6}})
        print response
        print response["body"]
        
        #getReportState
#        response=service.getReportState({"reportId":"be81065a009702ab629632ecf0d1f6bc"})
#        print response
#        print response["body"]
        
        
        
        
#        response=service.getReportState({"reportId":"ae17b433eef82ab5041969564ce3f9de"})
#        print response
#        response=service.getReportState({"reportId":"ae17b433eef82ab5041969564ce3f9de"})
#        print response
        #assert(response["header"]["desc"]=="success" and response["header"]["status"]==0)
        #getReportFileUrl
        response=service.getReportFileUrl({"reportId":"be81065a009702ab629632ecf0d1f6bc"})
        print response
        #assert(response["header"]["desc"]=="success" and response["header"]["status"]==0)
        
        
        print("###########################test report_service end.#################################")
    except Exception, e:
        print e
        tb.print_exc()

