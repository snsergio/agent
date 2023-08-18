#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#######################################################################################################################
versao = "versioncontrol-v5.00-PUB-5c07128-20230818165106"
#######################################################################################################################
import logging
import requests
import json
from lib import common as c
#######################################################################################################################
c.versionDict["versioncontrol"] = versao
#######################################################################################################################
# get version
# Check for metric collector version update
class version_update:
    def get_list_from_api(configDict):
        if configDict["apiUrl"] != "":
            c.apiList = json.loads(str(requests.get(configDict["apiUrl"] + "/vc/0").content)[2:-3])
            c.apiRepo = c.apiList["list_repo"]
            c.apiList = c.apiList["list_components"].replace("{", "").replace("}", "").split(",")
        return
    def compare_versions(configDict):
        version_update.get_list_from_api(configDict)
        for element in c.apiList:
            if "/" in element: component = element.split("/", 1)[1]
            else: component = element
            if "." in component: component = component.split(".")[0]
            if component in c.versionDict.keys():
                print(c.versionDict[component])            
        return




    # Update version control list with most recent list of components
    def check_components(newList):
        componentList = [
            "common",
            "metriccam",
            "metricconfig",
            "metricdisk",
            "metricdocker",
            "metricgpu",
            "metricnet",
            "metricping",
            "metricprocess",
            "metricsensor",
            "metricserver",
            "metricsysagent",
            "metrictop",
            "pushtogateway",
            "versioncontrol"]
        if len(newList) > 0:
            listUpd = tuple(set(newList).difference(set(componentList)))
            if len(listUpd) > 0:
                for newComp in range(len(listUpd)):
                    componentList.append(listUpd[newComp])
            listUpd = tuple(set(componentList).difference(set(newList)))
            if len(listUpd) > 0:
                for newComp in range(len(listUpd)):
                    componentList.remove(listUpd[newComp])
        versionDict = dict.fromkeys(componentList)     
        versionDict["versioncontrol"] = versao
        return versionDict
        #----------------------------------------------------------------------------------------------------------------------
