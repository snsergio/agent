#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#######################################################################################################################
versao = "metricline-v4.20-PUB-4d87eb0-20230508150250"
#######################################################################################################################
import logging
import time
from lib import common as c
#######################################################################################################################
c.versionDict["metricline"] = versao
#######################################################################################################################
class line_exec:
    # Execute line sensor metric collector
    def collect_line(getLine, lineURL):
        import json 
        lineout = ""
        if not c.logFirstRun: logging.info(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metricline version: {versao}")
        if getLine not in [None, ""] and len(lineURL) > 0:
            lineMetrics = {}
            lineSensorCount = 0
            for lineSensor in lineURL:
                a=c.exec_cmd(["curl", "-i", str(lineSensor)], c.debugMode)["output"]
                try: lineout = c.exec_cmd(["curl", "-i", str(lineSensor)], c.debugMode)["output"]
                except:
                    if not c.logFirstRun: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-line_exec.collect_line: Get lineSensor data error")
                if lineout != "": 
                    lineMetrics[lineSensorCount] = line_exec.line_metrics(lineout)
                    lineMetrics[lineSensorCount]["lineSensorUrl"] = lineSensor
                    lineSensorCount += 1
                else: lineMetrics[lineSensorCount] = 0
        return lineMetrics
        #----------------------------------------------------------------------------------------------------------------------
    # Prepare line sensor metrics data
    def line_metrics(lineout):
        resposta, respItem = {}, 0
        try: lineData = lineout.splitlines()
        except: lineData = 0
        else:
            if len(lineData) > 0:
                resposta = {
                    "lineSensorStatus": 0,
                    "lineSensorResponse": ""
                }
                for item in lineData:
                    if "refused" in item: resposta["lineSensorStatus"] = 1
                    if item[:4] == "HTTP":
                        sensorStatus = item.split()
                        if (sensorStatus[-1].strip().isnumeric()): resposta["lineSensorStatus"] = int(sensorStatus[-1].strip())
                        elif (sensorStatus[-2].strip().isnumeric()): resposta["lineSensorStatus"] = int(sensorStatus[-2].strip())
                        else: resposta["lineSensorStatus"] = 0
                resposta["lineSensorResponse"] = lineData[-1]
            else: resposta = 0
        return resposta
        #----------------------------------------------------------------------------------------------------------------------
