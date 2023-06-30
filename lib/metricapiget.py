#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#######################################################################################################################
versao = "metricapiget-v5.01-beta-test"
#######################################################################################################################
import logging
import time
from lib import common as c
#######################################################################################################################
c.versionDict["metricapiget"] = versao
#######################################################################################################################
class apiget_exec: 
    # Execute API GET metric collector - former line sensor
    def collect_apiget(getApiGet, apiUrl):
        apigetout, execerror = "", 0
        if not c.logFirstRun: logging.info(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metricapiget version: {versao}")
        if getApiGet and (len(apiUrl) > 0):
            getApiMetrics  = {}
            apiGetCount = 0
            for apiItem in apiUrl:
                apiTemp = {}
                try: apigetout = c.exec_cmd(["curl", "-i", str(apiItem), "--connect-timeout", "4"], c.debugMode)["output"]
                except:
                    if not c.logFirstRun: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-apiget_exec.collect_apiget: Get API data error")
                    execerror = 1
                if apigetout != "":
                    apiTemp["apiGetUrl"] = apiItem
                    apiTemp.update(apiget_exec.apiget_metrics(apigetout))
                else:
                    apiTemp["apiGetUrl"] = apiItem
                    apiTemp["apiGetExists"] = 0
                    apiTemp["apiGetStatus"] = 0
                    apiTemp["apiGetResponse"] = "timeout"
                getApiMetrics[apiGetCount] = apiTemp
                apiGetCount += 1
        getApiMetrics["apiGetExecError"] = execerror
        return getApiMetrics
        #----------------------------------------------------------------------------------------------------------------------
    # Prepare API GET metrics data
    def apiget_metrics(apigetout):
        resposta = {}
        try: apiGetData = apigetout.splitlines()
        except: apiGetData = 0
        else:
            if len(apiGetData) > 0:
                resposta = {
                    "apiGetExists": 0,
                    "apiGetStatus": 0,
                    "apiGetResponse": "timeout"
                }
                for item in apiGetData:
                    if any(retType in item.lower() for retType in ["refused", "found"]): resposta["apiGetExists"] = 1
                    if "HTTP" in item:
                        apiGetStatus = item.split(" ", 2)
                        if (apiGetStatus[1].strip().isnumeric()): 
                            resposta["apiGetStatus"] = int(apiGetStatus[1].strip())
                            resposta["apiGetResponse"] = apiGetStatus[-1].strip().lower()
                        elif (apiGetStatus[-1].strip().isnumeric()): resposta["apiGetStatus"] = int(apiGetStatus[-1].strip())
                    if resposta["apiGetResponse"] == "": resposta["apiGetResponse"] = apiGetData[-1]
            else: resposta = 0
        return resposta
        #----------------------------------------------------------------------------------------------------------------------
