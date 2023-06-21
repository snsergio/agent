#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#######################################################################################################################
versao = "metriccam-v5.00-beta-test"
#######################################################################################################################
import logging
import time
from lib import common as c
#######################################################################################################################
c.versionDict["metriccam"] = versao
#######################################################################################################################
class cam_exec:
    # Execute camera metric collector
    def collect_cam(getCam, camURL, camRestart = 0):
        import json 
        camout = ""
        if not c.logFirstRun: logging.info(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metriccam version: {versao}")
        if getCam not in [None, ""] and len(camURL) > 0:
            camMetrics = {}
            camCount = 0
            for item in camURL:
                camTemp = {}
                try: camout = json.loads(c.exec_cmd(["curl", str(item)], c.debugMode)["output"])
                except:
                    if not c.logFirstRun: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-cam_exec.collect_cam: Get camera data error")
                if camout != "":
                    camTemp["camUrl"] = item
                    camTemp.update(camTemp = cam_exec.cam_metrics(camout, camRestart, c.debugMode))
                else:
                    camTemp["camUrl"] = item
                    camTemp["status"] = 0
                    camTemp["camName"] = "no_cam"
                    camTemp["frameSeq"] = 0
                    camTemp["camHB"] = 0
                    camTemp["camHeight"] = 0
                    camTemp["camWidth"] = 0
                camMetrics[camCount] = camTemp
                camCount += 1
        else: camMetrics = 0
        return camMetrics
        #----------------------------------------------------------------------------------------------------------------------
    # Prepare camera metrics data
    def cam_metrics(camout, camRestart, debugMode):
        resposta, respItem = {}, 0
        try: camData = camout["data"]
        except: camData = 0
        if camData:
            for item in camData.keys():
                camDict = {}
                try: camDict["camName"] = camData[item]["input_name"]
                except: 
                    logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-cam_exec.cam_metrics: Camera [input_name] not set")
                    camDict["camName"] = "invalid"
                try: cStatus = camData[item]["status"].lower()
                except: 
                    logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-cam_exec.cam_metrics: Camera [status] not set")
                    cStatus = 0
                if cStatus == "ok": camDict["status"] = 1
                else: camDict["status"] = 0
                try: camDict["frameSeq"] = int(camData[item]["seq"])
                except: 
                    logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-cam_exec.cam_metrics: Camera [seq] not set")
                    camDict["frameSeq"] = -1
                try: camDict["camHB"] = float(camData[item]["time"])
                except: 
                    logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-cam_exec.cam_metrics: Camera [time] not set")
                    camDict["camHB"] = -1
                try: camDict["camHeight"] = int(camData[item]["height"])
                except: 
                    logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-cam_exec.cam_metrics: Camera [height] not set")
                    camDict["camHeight"] = -1
                try: camDict["camWidth"] = int(camData[item]["width"])
                except: 
                    logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-cam_exec.cam_metrics: Camera [width] not set")
                    camDict["camWidth"] = -1
                resposta[respItem] = camDict
                respItem += 1
                if camRestart and (time.time() - camDict["camHB"] > 30): 
                    if debugMode: 
                        logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-cam_exec.cam_metrics: Camera restart: {camRestart}")
                        logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-cam_exec.cam_metrics: Camera heartbeat delay: {(time.time() - camDict['camHB'])}")
                    cam_exec.camera_restart(camDict["camName"])
        else: resposta = 0
        return resposta
        #----------------------------------------------------------------------------------------------------------------------
    # Restart camera
    def camera_restart(camName):
        import subprocess
        if camName != 0: c.cameraCount += 1
        if cameraCount > 3:
            try: reCAM = subprocess.call('echo $SAMON | sudo -S systemctl restart run_flow.service', shell = True)
            except: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-cam_exec.camera_restart: Error restarting run_flow")
            logging.info(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-cam_exec.camera_restart: Camera restarted")
            cameraCount = 0
        return
        #----------------------------------------------------------------------------------------------------------------------
