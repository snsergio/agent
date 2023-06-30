#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#######################################################################################################################
versao = "metricjetson-v5.01-beta-test"
#######################################################################################################################
import logging
import time
import os
from lib import common as c
from jtop import jtop, JtopException
#######################################################################################################################
c.versionDict["metricjetson"] = versao
#######################################################################################################################
class jetson_exec:
    def collect_jetson(getJetson):
        jetsonout, jetsonExecError = {}, 0
        if getJetson:
            jetsonPath = "/usr/local/cuda/samples/1_Utilities/deviceQuery/deviceQuery"
            # isJetson = os.path.exists(jetsonPath)
            if os.path.exists(jetsonPath):
                if not c.logFirstRun: logging.info(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metricjetson version: {versao}")
                try: jetsonout = c.exec_cmd([jetsonPath], c.debugMode)["output"].splitlines()
                except: 
                    if not c.logFirstRun: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-jetson_exec.collect_jetson: Device Query execution error")
                    jetsonExecError = 1
        if jetsonout != 0: jetsonMetrics = jetson_exec.jetson_metrics(jetsonout, jetsonExecError)
        else: jetsonMetrics = 0
        return jetsonMetrics
        #----------------------------------------------------------------------------------------------------------------------
    def collect_jtop(resposta):
        try:
            with jtop() as jetson:
                if jetson.ok():
                    jtopout = jetson.stats
        except JtopException as e: 
            if not c.logFirstRun: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-jetson_exec.collect_jtop: jtop error")
            logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-jetson_exec.collect_jtop: jtop error: {e}")
            resposta["jtopExecError"] = 1
        else:
            resposta["cpuTotalCount"] = 0
            resposta["jtopExecError"] = 0
            for k, v in jtopout.items():
                if (len(k) <= 5) and ("CPU" in k): resposta["cpuTotalCount"] += 1
                if (len(k) == 3) and ("GPU" in k): resposta["gpuUse"] = int(v)
                if ("Fan" in k): resposta["fanPercent"] = int(v)
                if ("TOT" in k): resposta["powerTotal"] = int(v)
                if ("thermal" in k): resposta["powerThermal"] = int(v)
                if ("RAM" in k): resposta["ramUsed"] = float(v)
                if ("Temp CPU" in k): resposta["tempCPU"] = float(v)
                if ("Temp GPU" in k): resposta["tempGPU"] = float(v)
                if ("Tboard" in k): resposta["tempBoard"] = float(v)
                if ("iwlwifi" in k): resposta["tempWifi"] = float(v)
                if ("nvp" in k): resposta["nvpModel"] = str(v)
                if (k == "time"): resposta["time"] = v.timestamp()
                if (k == "uptime"): resposta["uptime"] = v.total_seconds()
        return resposta
        #----------------------------------------------------------------------------------------------------------------------
    def jetson_metrics(jetsonData, jetsonExecError):
        resposta = {
            "jetsonExecError": jetsonExecError,
            "card": "",
            "driver": "",
            "cuda": "",
            "gpuName": "",
            "memTotalMB": 0}
        for item in range(len(jetsonData)):
            if (4 <= item <= 7) and ("Device" in jetsonData[item]): resposta["card"] = jetsonData[item].split(":")[0].split()[-1].strip()
            if (5 <= item <= 8) and ("Driver" in jetsonData[item]) and ("CUDA" in jetsonData[item]): resposta["driver"] = jetsonData[item].split()[-1].strip()
            if (5 <= item <= 8) and ("Driver" in jetsonData[item]) and ("CUDA" in jetsonData[item]): resposta["cuda"] = jetsonData[item].split("/")[1].split()[-1]
            if (5 <= item <= 7) and ("Device" in jetsonData[item]): resposta["gpuName"] = str(jetsonData[item].split(":")[-1].strip().replace("'","").replace('"', ''))
            if (5 <= item <= 10) and ("amount" in jetsonData[item]) and ("global" in jetsonData[item]): resposta["memTotalMB"] = int(jetsonData[item].split(":")[1].split()[0])
        try: a = jetson_exec.collect_jtop(resposta)
        except: 
            if not c.logFirstRun: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-jetson_exec.collect_jetson: Device Query execution error")
            a["jtopExecError"] = 1
        resposta.update(a)
        return resposta
        #----------------------------------------------------------------------------------------------------------------------
