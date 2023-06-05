#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#######################################################################################################################
versao = "metricprocess-v4.20-PUB-4d87eb0-20230508150250"
#######################################################################################################################
import logging
import time
from lib import common as c
#######################################################################################################################
c.versionDict["metricprocess"] = versao
#######################################################################################################################
class process_exec:
    # Execute Ubuntu Processes metric collector
    def collect_process(getProcess, processList):
        processout = ""
        if getProcess:
            if not c.logFirstRun: logging.info(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metricprocess version: {versao}")
            try: processout = c.exec_cmd(["ps", "-fA"], c.debugMode)["output"].splitlines()
            except: 
                if not c.logFirstRun: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-Get Metrics: PS execution error")
        if processout != "": processMetrics = process_exec.process_metrics(processout, processList)
        else: processMetrics = 0
        return processMetrics
        #----------------------------------------------------------------------------------------------------------------------
    def process_metrics(processData, processNames):
        resposta, processCount, runProcess, processPID = {}, 0, [], []
        if c.debugMode: logging.debug(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-Process Metrics: Process List: {processNames}")
        if processNames != 0:
            for task in range(len(processNames)):
                resposta[processCount] = {
                    "processCfg": processNames[task],
                    "user": "none",
                    "pid": 0,
                    "cpu": 0.0,
                    "mem": 0.0,
                    "time": 0.0,
                    "processActive": 0,
                    "cmd": "none"}
                for element in range(1, len(processData)):
                    evalProcess = processData[element].split()
                    hourItem = 0
                    for item in range(len(evalProcess)):
                        if evalProcess[item].count(":") >= 2:
                            break
                        hourItem += 1
                    procCmd = ' '.join(evalProcess[hourItem + 1:])
                    if processNames[task] in procCmd:
                        runProcess.append(processNames[task])
                        if evalProcess[1] not in set(processPID):
                            try: pTime = evalProcess[hourItem].split(":")
                            except: pTime = [0]
                            try: pData = c.exec_cmd(["ps", "-p", evalProcess[1], "-o", "%cpu,%mem"], c.debugMode)["output"].splitlines()[1].split()
                            except: pData = [0, 0]
                            if pTime[0].count("-") > 0:
                                timeVal = pTime[0].split("-")
                                if timeVal[0].isnumeric: dd = int(timeVal[0])*24
                                if timeVal[1].isnumeric: dd += int(timeVal[1])
                            elif pTime[0].isnumeric: dd = int(pTime[0])
                            else: dd = 0
                            try: mVal = int(pTime[1])*60
                            except: mVal = 0
                            try: sVal = int(pTime[2])
                            except: sVal = 0
                            try: cpuVal = str(pData[0]).replace(',', '.')
                            except:
                                if pData[0].isnumeric: cpuVal = float(pData[0])
                                else: cpuVal = 0
                            try: memVal = str(pData[1]).replace(',', '.')
                            except:
                                if pData[1].isnumeric: memVal = float(pData[1])
                                else: memVal = 0
                            resposta[processCount] = {
                                "processCfg": processNames[task],
                                "user": evalProcess[0],
                                "pid": int(evalProcess[1]),
                                "cpu": float(cpuVal),
                                "mem": float(memVal),
                                "time": dd*3600 + mVal*60 + sVal,
                                "processActive": 1,
                                "cmd": procCmd}
                            processPID.append(evalProcess[1])
                            processCount += 1
        else: resposta = 0
        if processCount == 0:
            if len(processNames) > 0: 
                if not c.logFirstRun: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-Process Metrics: No active Processes")
        if c.debugMode: logging.debug(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-Process Metrics: Active Processes: {processCount}")
        resposta["missingProcess"] = list((set(processNames).difference(set(runProcess))))
        return resposta
        #----------------------------------------------------------------------------------------------------------------------
