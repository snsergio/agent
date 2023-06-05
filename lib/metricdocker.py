#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#######################################################################################################################
versao = "metricdocker-v4.20-PUB-4d87eb0-20230508150250"
#######################################################################################################################
import logging
import time
from lib import common as c
#######################################################################################################################
c.versionDict["metricdocker"] = versao
#######################################################################################################################
class docker_exec:
    # Execute docker metric collector
    def collect_docker(getDocker, eyeflowDockerList, eyeflowDockerExcept):
        resposta = {
            "docker": 0,
            "eyeflow": 0}
        if getDocker:
            if not c.logFirstRun: logging.info(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metricdocker version: {versao}")
            try: dockerout = c.exec_cmd(["docker", "ps", "--no-trunc"], c.debugMode)["output"].splitlines()
            except: 
                if not c.logFirstRun: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-docker_exec.collect_docker: Docker execution error")
        if len(dockerout) > 0: resposta["docker"] = docker_exec.docker_metrics(dockerout)
        else: resposta["docker"] = 0
        eyeflowSvc = 0
        if resposta["docker"] != 0:
            efResposta = {}
            if "all" not in eyeflowDockerList:
                for element in range(len(resposta["docker"])):
                    if not (eyeflowDockerList is None or any(element is None for element in eyeflowDockerList)):
                        for wordAdd in eyeflowDockerList:
                            if wordAdd in resposta["docker"][element]["names"]:
                                if not (eyeflowDockerExcept is None or any(element is None for element in eyeflowDockerExcept)):
                                    if not any(wordDel in resposta["docker"][element]["names"] for wordDel in eyeflowDockerExcept):
                                        efResposta[eyeflowSvc] = resposta["docker"][element]
                                        efResposta[eyeflowSvc]["efname"] = wordAdd
                                        eyeflowSvc += 1
                                else:
                                    efResposta[eyeflowSvc] = resposta["docker"][element]
                                    efResposta[eyeflowSvc]["efname"] = wordAdd
                                    eyeflowSvc += 1
            else:
                for element in range(len(resposta["docker"])):
                    if not (eyeflowDockerExcept is None or any(element is None for element in eyeflowDockerExcept)):
                        if not any(wordDel in resposta["docker"][element]["names"] for wordDel in eyeflowDockerExcept):
                            efResposta[eyeflowSvc] = resposta["docker"][element]
                            efResposta[eyeflowSvc]["efname"] = "all"
                            eyeflowSvc += 1
                    else:
                        efResposta[eyeflowSvc] = resposta["docker"][element]
                        efResposta[eyeflowSvc]["efname"] = "all"
                        eyeflowSvc += 1

                resposta["eyeflow"] = efResposta
        else: resposta["eyeflow"] = 0
        return resposta
        #----------------------------------------------------------------------------------------------------------------------
    def docker_metrics(dockerout):
        resposta = {}
        if len(dockerout) > 1:
            keyList = dockerout[0].split("  ")
            keyList = [keyName.lower().strip() for keyName in keyList if keyName != ""]
            for element in range(1, len(dockerout)):
                cmdTrim, imgData = [], {}
                tmp1 = dockerout[element].split("  ")
                for n in range(len(tmp1)):
                    if tmp1[n] != "": cmdTrim.append(tmp1[n].strip().replace('"',''))
                if len(cmdTrim) < 7:
                    cmdTrim.append(cmdTrim[-1])
                    cmdTrim[-2] = ""
                try: indx = keyList.index("image")
                except: imgData["image"] = ""
                else: imgData["image"] = cmdTrim[indx]
                try: indx = keyList.index("command")
                except: imgData["command"] = ""
                else: imgData["command"] = cmdTrim[indx]
                try: indx = keyList.index("created")
                except: imgData["created"] = ""
                else: imgData["created"] = docker_exec.convert_texttime(cmdTrim[indx].split())
                try: indx = keyList.index("status")
                except: 
                    imgData["status"] = ""
                    imgData["statusTime"] = 0
                else:
                    statusList = cmdTrim[indx].split()
                    imgData["status"] = statusList[0].lower()
                    statusAge = statusList[1:]
                    statusAge.append("ago")
                    imgData["statusTime"] = docker_exec.convert_texttime(statusAge)
                try: indx = keyList.index("ports")
                except: imgData["ports"] = ""
                else: imgData["ports"] = cmdTrim[indx]
                try: indx = keyList.index("names")
                except: imgData["names"] = ""
                else: imgData["names"] = cmdTrim[indx]
                resposta[element - 1] = imgData
        else: resposta = 0
        return resposta
        #----------------------------------------------------------------------------------------------------------------------
    def convert_texttime(textdata):
        if len(textdata) == 3:
            if textdata[0].isdigit(): createdData = int(textdata[0])
            createdData *= docker_exec.get_multiplier(textdata)
        elif len(textdata) > 3:
            for n in range(len(textdata)):
                if textdata[n].isdigit(): createdData = int(textdata[n])
                elif textdata[n] == "a" or textdata[n] == "an": createdData = 1
            createdData *= docker_exec.get_multiplier(textdata)
        return createdData
        #----------------------------------------------------------------------------------------------------------------------
    def get_multiplier(textdata):
        createdData = 0
        if textdata[-1] == "ago" and textdata[-2] == "ago": textdata = textdata[:-1]
        if textdata[-1] == "ago":
            if "second" in textdata[-2]: createdData = 1
            if "minute" in textdata[-2]: createdData = 60
            if "hour" in textdata[-2]: createdData = 60 * 60
            if "day" in textdata[-2]: createdData = 60 * 60 * 24
            if "week" in textdata[-2]: createdData = 60 * 60 * 24 * 7
            if "month" in textdata[-2]: createdData = 60 * 60 * 24 * 30
            if "year" in textdata[-2]: createdData = 60 * 60 * 24 * 365
        return createdData
        #----------------------------------------------------------------------------------------------------------------------
