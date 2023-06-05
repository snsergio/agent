#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#######################################################################################################################
versao = "metricconfig-v4.20-PUB-4d87eb0-20230508150250"
#######################################################################################################################
import logging
import time
from lib import common as c
#######################################################################################################################
c.versionDict["metricconfig"] = versao
#######################################################################################################################
class config_setup:
    # SETUP ---------------------------------------------------------------------------------------------------------------
    #######################################################################################################################
    # configFileName: Default configuration file name. Typically 'collector-config.yaml'
    #   Edit the configuration file accordingly to reflect metrics to collect at the station being executed
    #   Path to Configuration file is set by environment variable $CONFIGPATH or defaults to './'
    #######################################################################################################################
    configDict = {}
    # Get config file
    def get_config():
        import os
        import yaml
        from pathlib import Path
        configPath = os.environ.get('CONFIGPATH')
        metric_attributes.resposta["hostName"] = "myhost"
        if configPath == None: 
            logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-config_setup.get_config: Env var CONFIGPATH not set, changing to CWD")
            configPath = "./"
        if configPath[-1:] != "/": configPath += "/"
        if os.path.isfile(configPath + c.configFileName): config_setup.configDict = yaml.safe_load(Path(configPath + c.configFileName).read_text())
        else: 
            logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-config_setup.get_config: {c.configFileName} not found at {configPath}")
            print(f"[ERROR] {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-config_setup.get_config: {c.configFileName} not found at {configPath}")
            exit(1)
        try: 
            c.logPath = config_setup.configDict["path"]["logPath"]
            c.scriptPath = config_setup.configDict["path"]["scriptFile"]
        except: 
            logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-config_setup.get_config: Setup path information not correctly set")
            logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-config_setup.get_config: Setup file path/logpath set to {c.logPath}")
            logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-config_setup.get_config: Setup file path/scriptFile set to {c.scriptPath}")
            c.logPath = configPath
        if c.logPath[-1:] != "/": c.logPath += "/"
        try: metric_attributes.resposta["hostName"] = os.uname()[1].lower()
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-config_setup.get_config: Hostname not defined, set to {metric_attributes.resposta['hostName']}")
        if metric_attributes.resposta["hostName"] == None or metric_attributes.resposta["hostName"] == "": metric_attributes.resposta["hostName"] = "notset"
        return metric_attributes.validate(config_setup.configDict)
        #----------------------------------------------------------------------------------------------------------------------
class metric_attributes:
    resposta = {}
    # Get customer information from configuration file
    def get_custom(configDict):
        metric_attributes.resposta["customerName"] = "customer"
        metric_attributes.resposta["captureInterval"] = 15
        metric_attributes.resposta["stationIpList"] = []
        try: metric_attributes.resposta["customerName"] = configDict["custom"]["customerName"]
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_custom: custom/customerName not set. Assuming 'customer'")
        try: metric_attributes.resposta["captureInterval"] = configDict["custom"]["captureInterval"]
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_custom: custom/captureInterval not set")
        if not isinstance(metric_attributes.resposta["captureInterval"], int):
            if metric_attributes.resposta["captureInterval"][-1:] == "s": 
                metric_attributes.resposta["captureInterval"] = metric_attributes.resposta["captureInterval"][:-1]
        if str(metric_attributes.resposta["captureInterval"]).isdigit(): 
            metric_attributes.resposta["captureInterval"] = int(metric_attributes.resposta["captureInterval"])
        else: 
            logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_custom: custom/captureInterval must be in format: <seconds[s]>. Assuming 30s")
            metric_attributes.resposta["captureInterval"] = 30
        if metric_attributes.resposta["captureInterval"] < 5: 
            logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_custom: custom/captureInterval must be >= 5s. Assuming 5s")
            metric_attributes.resposta["captureInterval"] = 5
        try: metric_attributes.resposta["stationIpList"] = configDict["custom"]["StationIP"]
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_custom: custom/stationIP not set")
        if metric_attributes.resposta["stationIpList"] == None or len(metric_attributes.resposta["stationIpList"]) < 1: 
            metric_attributes.resposta["stationIpList"] = []
        return
        #----------------------------------------------------------------------------------------------------------------------
    # Get environment information from configuration file
    def get_environment(configDict):
        metric_attributes.resposta["pushUrl"] = None
        metric_attributes.resposta["pushUrl2"] = None
        metric_attributes.resposta["camUrl"] = None
        metric_attributes.resposta["lineSensrorUrl"] = None
        metric_attributes.resposta["pingList"] = []
        metric_attributes.resposta["processNames"] = []
        metric_attributes.resposta["eyeflowDocker"] = []
        metric_attributes.resposta["eyeflowDockerExcept"] = []
        metric_attributes.resposta["topProcessNumber"] = 0
        try: metric_attributes.resposta["pushUrl"] = configDict["environment"]["pushUrl"]
        except: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_environment: environment/pushUrl not set")
        try: metric_attributes.resposta["pushUrl2"] = configDict["environment"]["pushUrl2"]
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_environment: environment/pushUrl2 not set")
        try: metric_attributes.resposta["camUrl"] = configDict["environment"]["camUrl"]
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_environment: environment/camUrl not set")
        try: metric_attributes.resposta["lineSensrorUrl"] = configDict["environment"]["lineSensrorUrl"]
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_environment: environment/lineSensrorUrl not set")
        try: metric_attributes.resposta["pingList"] = configDict["environment"]["pingList"]
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_environment: environment/pingList not set")
        try: metric_attributes.resposta["processNames"] = configDict["environment"]["processNames"]
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_environment: environment/processNames not set")
        try: metric_attributes.resposta["eyeflowDocker"] = configDict["environment"]["eyeflowDocker"]
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_environment: environment/eyeflowDocker not set")
        try: metric_attributes.resposta["eyeflowDockerExcept"] = configDict["environment"]["eyeflowDockerExcept"]
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_environment: environment/eyeflowDockerExcept not set")
        try: metric_attributes.resposta["topProcessNumber"] = int(configDict["environment"]["topProcessNumber"])
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_environment: environment/topProcessNumber not set")
        return
        #----------------------------------------------------------------------------------------------------------------------
    # Get TLS information from configuration file
    def get_tls(configDict):
        metric_attributes.resposta["tls1"] = False
        metric_attributes.resposta["tls2"] = False
        metric_attributes.resposta["user1"] = ""
        metric_attributes.resposta["user2"] = ""
        metric_attributes.resposta["pass1"] = ""
        metric_attributes.resposta["pass2"] = ""
        import base64
        try: metric_attributes.resposta["tls1"] = configDict["tls"]["pushUrl_TLS"]
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_tls: tls/pushUrl_TLS not set")
        try: metric_attributes.resposta["tls2"] = configDict["tls"]["pushUrl2_TLS"]
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_tls: tls/pushUrl2_TLS not set")
        if metric_attributes.resposta["tls1"]:
            try: metric_attributes.resposta["user1"] = configDict["tls"]["pushUrl_TLS_Username"]
            except: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_tls: tls/pushUrl_TLS_Username not set")
            try: metric_attributes.resposta["pass1"] = base64.b64decode(configDict["tls"]["pushUrl_TLS_Password"]).decode("utf-8")
            except: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_tls: tls/pushUrl_TLS_Password not set")
            if metric_attributes.resposta["user1"] == None or metric_attributes.resposta["user1"] == "":
                logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_tls: tls/pushUrl_TLS_Username not set, disabling TLS")
                metric_attributes.resposta["tls1"], metric_attributes.resposta["user1"] = 0, ""
            if metric_attributes.resposta["pass1"] == None or metric_attributes.resposta["pass1"] == "":
                logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_tls: tls/pushUrl_TLS_Password not set, disabling TLS")
                metric_attributes.resposta["tls1"], metric_attributes.resposta["pass1"] = 0, ""
        if metric_attributes.resposta["tls2"]:
            try: metric_attributes.resposta["user2"] = configDict["tls"]["pushUrl2_TLS_Username"]
            except: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_tls: tls/pushUrl2_TLS_Username not set")
            try: metric_attributes.resposta["pass2"] = base64.b64decode(configDict["tls"]["pushUrl2_TLS_Password"]).decode("utf-8")
            except: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_tls: tls/pushUrl2_TLS_Password not set")
            if metric_attributes.resposta["user2"] == None or metric_attributes.resposta["user2"] == "":
                logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_tls: tls/pushUrl2_TLS_Username not set, disabling TLS")
                metric_attributes.resposta["tls2"], metric_attributes.resposta["user2"] = 0, ""
            if metric_attributes.resposta["pass2"] == None or metric_attributes.resposta["pass2"] == "":
                logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_tls: tls/pushUrl2_TLS_Password not set, disabling TLS")
                metric_attributes.resposta["tls2"], metric_attributes.resposta["pass2"] = 0, ""
        return 
        #----------------------------------------------------------------------------------------------------------------------
    # Get capture_metrics information from configuration file
    def get_capture(configDict):
        metric_attributes.resposta["getBackup"] = False
        metric_attributes.resposta["getCam"] = False
        metric_attributes.resposta["getDisk"] = False
        metric_attributes.resposta["getDocker"] = False
        metric_attributes.resposta["getGpuNvidia"] = False
        metric_attributes.resposta["lineSensor"] = False
        metric_attributes.resposta["getNetwork"] = False
        metric_attributes.resposta["getIpPing"] = False
        metric_attributes.resposta["getProcess"] = False
        metric_attributes.resposta["getTopProcess"] = False
        metric_attributes.resposta["getSelfIp"] = False
        metric_attributes.resposta["getSensor"] = False
        metric_attributes.resposta["getSysAgent"] = False
        metric_attributes.resposta["getServer"] = False
        try: metric_attributes.resposta["getBackup"] = bool(configDict["captureMetrics"]["backup"])
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_capture: captureMetrics/backup not set. Assuming 'false'")
        try: metric_attributes.resposta["getCam"] = bool(configDict["captureMetrics"]["camera"])
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_capture: captureMetrics/camera not set. Assuming 'false'")
        try: metric_attributes.resposta["getDisk"] = bool(configDict["captureMetrics"]["disk"])
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_capture: captureMetrics/disk not set. Assuming 'false'")
        try: metric_attributes.resposta["getDocker"] = bool(configDict["captureMetrics"]["docker"])
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_capture: captureMetrics/docker not set. Assuming 'false'")
        try: metric_attributes.resposta["getGpuNvidia"] = bool(configDict["captureMetrics"]["gpuNvidia"])
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_capture: captureMetrics/gpuNvidia not set. Assuming 'false'")
        try: metric_attributes.resposta["lineSensor"] = bool(configDict["captureMetrics"]["lineSensor"])
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_capture: captureMetrics/lineSensor not set. Assuming 'false'")
        try: metric_attributes.resposta["getNetwork"] = bool(configDict["captureMetrics"]["network"])
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_capture: captureMetrics/network not set. Assuming 'false'")
        try: metric_attributes.resposta["getIpPing"] = bool(configDict["captureMetrics"]["ipPing"])
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_capture: captureMetrics/ipPing not set. Assuming 'false'")
        try: metric_attributes.resposta["getProcess"] = bool(configDict["captureMetrics"]["process"])
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_capture: captureMetrics/process not set. Assuming 'false'")
        try: metric_attributes.resposta["getTopProcess"] = bool(configDict["captureMetrics"]["topProcess"])
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_capture: captureMetrics/topProcess not set. Assuming 'false'")
        try: metric_attributes.resposta["getSelfIp"] = bool(configDict["captureMetrics"]["selfIP"])
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_capture: captureMetrics/selfIP not set. Assuming 'false'")
        try: metric_attributes.resposta["getSensor"] = bool(configDict["captureMetrics"]["sensor"])
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_capture: captureMetrics/sensor not set. Assuming 'false'")
        try: metric_attributes.resposta["getSysAgent"] = bool(configDict["captureMetrics"]["sysAgent"])
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_capture: captureMetrics/sysAgent not set. Assuming 'false'")
        try: metric_attributes.resposta["getServer"] = bool(configDict["captureMetrics"]["server"])
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_capture: captureMetrics/server not set. Assuming 'false'")
        return
        #----------------------------------------------------------------------------------------------------------------------
    # Get backup information from configuration file
    def get_backup(configDict):
        import os
        metric_attributes.resposta["backupFolder"] = "./"
        metric_attributes.resposta["backupFrequency"] = "1m"
        metric_attributes.resposta["backupPrefix"] = ""
        metric_attributes.resposta["backupSuffix"] = ""
        try: metric_attributes.resposta["backupFolder"] = configDict["backup"]["folder"]
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_restart: backup/folder not set")
        try: metric_attributes.resposta["backupFrequency"] = configDict["backup"]["frequency"]
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_restart: backup/frequency not set")
        try: metric_attributes.resposta["backupPrefix"] = configDict["backup"]["filePrefix"]
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_restart: backup/filePrefix not set")
        try: metric_attributes.resposta["backupSuffix"] = configDict["backup"]["fileSuffix"]
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_restart: backup/fileSuffix not set")
        return
        #----------------------------------------------------------------------------------------------------------------------
    # Get restart information from configuration file
    def get_restart(configDict):
        import os
        metric_attributes.resposta["camRestart"] = False
        metric_attributes.resposta["sysAgentRestart"] = False
        metric_attributes.resposta["suAccess"] = False
        try: metric_attributes.resposta["camRestart"] = bool(configDict["restart"]["camRestart"])
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_restart: restart/camRestart not set")
        try: metric_attributes.resposta["sysAgentRestart"] = bool(configDict["restart"]["sysAgentRestart"])
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_restart: restart/sysAgentRestart not set")
        try: os.environ["SAMON"] = configDict["restart"]["suAccess"]
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_restart: restart/suAccess not set")
        if (metric_attributes.resposta["camRestart"] or 
            metric_attributes.resposta["sysAgentRestart"]) and (configDict["restart"]["suAccess"] in [None, ""]):
            logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-Setup: required restart/suAccess not set")
        return
        #----------------------------------------------------------------------------------------------------------------------
    # Get mescelaneous information from configuration file
    def get_misc(configDict):
        metric_attributes.resposta["metricDetails"] = "light"
        metric_attributes.resposta["debugMode"] = False
        try: metric_attributes.resposta["metricDetails"] = configDict["metricDetails"].lower()
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_misc: metricDetails not set")
        try: metric_attributes.resposta["debugMode"] = bool(configDict["debugMode"])
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_misc: debugMode not set. Assuming false")
        if metric_attributes.resposta["metricDetails"] == "full": metric_attributes.resposta["metricDetails"] = True
        elif metric_attributes.resposta["metricDetails"] == "light": metric_attributes.resposta["metricDetails"] = False
        return
        #----------------------------------------------------------------------------------------------------------------------
    # Get update information from configuration file
    def get_update(configDict):
        import os
        metric_attributes.resposta["apiUrl"] = ""
        metric_attributes.resposta["apiAccessToken"] = ""
        metric_attributes.resposta["autoRestart"] = False
        metric_attributes.resposta["autoUpdate"] = False
        try: metric_attributes.resposta["apiUrl"] = configDict["update"]["apiUrl"]
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}- metric_attributes.get_update: update/apiUrl not set")
        try: metric_attributes.resposta["apiAccessToken"] = configDict["update"]["apiAccessToken"]
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_update: update/apiAccessToken not set")
        try: metric_attributes.resposta["autoRestart"] = bool(configDict["update"]["autoRestart"])
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_restart: update/autoRestart not set")
        try: metric_attributes.resposta["autoUpdate"] = bool(configDict["update"]["autoUpdate"])
        except: logging.warning(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.get_restart: update/autoUpdate not set")
        return
        #----------------------------------------------------------------------------------------------------------------------
    # Validate configuration file paramenters
    def validate(configDict):
        metric_attributes.get_custom(configDict)
        metric_attributes.get_environment(configDict)
        metric_attributes.get_tls(configDict)
        metric_attributes.get_capture(configDict)
        metric_attributes.get_backup(configDict)
        metric_attributes.get_restart(configDict)
        metric_attributes.get_misc(configDict)
        metric_attributes.get_update(configDict)
        metric_attributes.resposta["metricconfig_version"] = str(versao)
        if metric_attributes.resposta["debugMode"]:
            logging.debug(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metric_attributes.validate: configDict: {metric_attributes.resposta}")
        return metric_attributes.resposta
        #----------------------------------------------------------------------------------------------------------------------
