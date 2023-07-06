#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#######################################################################################################################
versao = "metricjetson-v5.02-PUB-f0875b2-20230703130653"
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
        jetsonMetrics = {}
        if getJetson:
            if not c.logFirstRun: logging.info(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metricjetson version: {versao}")
            jetsonPath = "/usr/local/cuda/samples/1_Utilities/deviceQuery/deviceQuery"
            jetsonPath2 = "/opt/eyeflow/monitor/jetson/deviceQuery"
            if os.path.exists(jetsonPath):
                try: jetsonout = c.exec_cmd([jetsonPath], c.debugMode)["output"].splitlines()
                except: 
                    if not c.logFirstRun: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-jetson_exec.collect_jetson: Device Query execution error")
                    jetsonExecError = 1
            elif os.path.exists(jetsonPath2):
                try: jetsonout = c.exec_cmd([jetsonPath2], c.debugMode)["output"].splitlines()
                except: 
                    if not c.logFirstRun: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-jetson_exec.collect_jetson: Device Query execution error on path2")
                    jetsonExecError = 1
        jetsonMetrics = jetson_exec.jetson_metrics(jetsonout, jetsonExecError)
        return jetsonMetrics
        #----------------------------------------------------------------------------------------------------------------------
    def collect_jtop(resposta):
        resposta = {"cpuTotalCount": 0,
                    "jtopExecError": 0,
                    "gpuUse": 0,
                    "fanPercent": 0,
                    "powerTotal": 0,
                    "powerThermal": 0,
                    "ramUsed": 0,
                    "tempCPU": 0,
                    "tempGPU": 0,
                    "tempBoard": 0,
                    "tempWifi": 0,
                    "nvpModel": "",
                    "time": 0,
                    "uptime": 0}
        readOk = 0
        with jtop() as jetson:
            while not readOk:
                if jetson.ok():
                    try: 
                        jtopout = jetson.stats
                        readOk = 1
                    except JtopException as e: 
                        if not c.logFirstRun: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-jetson_exec.collect_jtop: jtop error")
                        logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-jetson_exec.collect_jtop: jtop error: {e}")
                        resposta["jtopExecError"] = 1
        for k, v in jtopout.items():
            if (len(k) <= 5) and ("CPU" in k):
                try: resposta["cpuTotalCount"] += 1
                except: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-jetson_exec.collect_jtop: jtop error on CPU")
            if (len(k) == 3) and ("GPU" in k): 
                try: resposta["gpuUse"] = int(v)
                except: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-jetson_exec.collect_jtop: jtop error on GPU")
            if ("Fan" in k):
                try: resposta["fanPercent"] = int(v)
                except: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-jetson_exec.collect_jtop: jtop error on FAN")
            if ("TOT" in k):
                try: resposta["powerTotal"] = int(v)
                except: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-jetson_exec.collect_jtop: jtop error on PowerTotal")
            if ("thermal" in k):
                try: resposta["powerThermal"] = int(v)
                except: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-jetson_exec.collect_jtop: jtop error on PowerThermal")
            if ("RAM" in k):
                try: resposta["ramUsed"] = float(v)
                except: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-jetson_exec.collect_jtop: jtop error on RAM")
            if ("Temp CPU" in k):
                try: resposta["tempCPU"] = float(v)
                except: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-jetson_exec.collect_jtop: jtop error on TempCPU")
            if ("Temp GPU" in k):
                try: resposta["tempGPU"] = float(v)
                except: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-jetson_exec.collect_jtop: jtop error on TempGPU")
            if ("Tboard" in k):
                try: resposta["tempBoard"] = float(v)
                except: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-jetson_exec.collect_jtop: jtop error on TempBD")
            if ("iwlwifi" in k):
                try: resposta["tempWifi"] = float(v)
                except: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-jetson_exec.collect_jtop: jtop error on TempWIFI")
            if ("nvp" in k):
                try: resposta["nvpModel"] = str(v)
                except: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-jetson_exec.collect_jtop: jtop error on NVP")
            if (k == "time"):
                try: resposta["time"] = v.timestamp()
                except: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-jetson_exec.collect_jtop: jtop error on TIME")
            if (k == "uptime"):
                try: resposta["uptime"] = v.total_seconds()
                except: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-jetson_exec.collect_jtop: jtop error on UPTIME")
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
        if len(jetsonData) > 1:
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
