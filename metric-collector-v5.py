#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#######################################################################################################################
versao = "metric-collector-v5.00-beta-test"
#######################################################################################################################
import logging 
#######################################################################################################################
# get metrics
def get_metrics(configDict):
        resposta = {
            "apiGetMetrics": 0,
            "bkpMetrics": 0,
            "camMetrics": 0,
            "diskMetrics": 0,
            "dockerMetrics": 0,
            "gpuMetrics": 0,
            "pingMetrics": 0,
            "monOsProcMetrics": 0,
            "netMetrics": 0,
            "remoteOpenMetrics": 0,
            "selfIpMetrics": 0,
            "sensorMetrics": 0,
            "serverMetrics": 0,
            "sysAgentMetrics": 0,
            "topMetrics": 0}
        collLatency = {
            "apiGetMetrics": 0,
            "bkpMetrics": 0,
            "camMetrics": 0,
            "diskMetrics": 0,
            "dockerMetrics": 0,
            "gpuMetrics": 0,
            "pingMetrics": 0,
            "monOsProcMetrics": 0,
            "netMetrics": 0,
            "remoteOpenMetrics": 0,
            "selfIpMetrics": 0,
            "sensorMetrics": 0,
            "serverMetrics": 0,
            "sysAgentMetrics": 0,
            "topMetrics": 0}
        if configDict["getNetwork"]:
            from lib import metricnet as mn
            net1 = mn.net_exec.get_net()
            net1start = time.time()
        if configDict["getApiGet"]:
            inicio = time.time()
            from lib import metricapiget as ag
            resposta["apiGetMetrics"] = ag.apiget_exec.collect_apiget(
                configDict["getApiGet"], 
                configDict["apiUrl"])
            collLatency["apiGetMetrics"] = time.time() - inicio
        if configDict["getBackup"]:
            inicio = time.time()
            from lib import metricbackup as bkp
            resposta["bkpMetrics"] = bkp.backup_exec.collect_backup(
                configDict["getBackup"], 
                configDict["backupFolder"], 
                configDict["backupPrefix"], 
                configDict["backupSuffix"],
                configDict["backupFrequency"])
            collLatency["bkpMetrics"] = time.time() - inicio
        if configDict["getCam"]:
            inicio = time.time()
            from lib import metriccam as cam
            resposta["camMetrics"] = cam.cam_exec.collect_cam(
                configDict["getCam"], 
                configDict["camUrl"], 
                configDict["camRestart"])
            collLatency["camMetrics"] = time.time() - inicio
        if configDict["getDisk"]:
            inicio = time.time()
            from lib import metricdisk as dsk
            resposta["diskMetrics"] = dsk.disk_exec.collect_disk(
                configDict["getDisk"])
            collLatency["diskMetrics"] = time.time() - inicio
        if configDict["getDocker"]:
            inicio = time.time()
            from lib import metricdocker as dock
            retorno = dock.docker_exec.collect_docker(
                configDict["getDocker"], 
                configDict["dockerList"],
                configDict["dockerExceptList"])
            resposta["dockerMetrics"] = retorno
            collLatency["dockerMetrics"] = time.time() - inicio
        if configDict["getGpuNvidia"]:
            inicio = time.time()
            from lib import metricgpu as gpu
            resposta["gpuMetrics"] = gpu.gpu_exec.collect_gpu(
                configDict["getGpuNvidia"])
            collLatency["gpuMetrics"] = time.time() - inicio
        if configDict["getIpPing"]:
            inicio = time.time()
            from lib import metricping as ip
            resposta["pingMetrics"] = ip.ping_exec.collect_ping(
                configDict["getIpPing"], 
                configDict["ipPingList"])
            collLatency["pingMetrics"] = time.time() - inicio
        if configDict["getMonOsProc"]:
            inicio = time.time()
            from lib import metricmonosproc as mop
            resposta["monOsProcMetrics"] = mop.mon_os_proc_exec.collect_mon_os_proc(
                configDict["getMonOsProc"], 
                configDict["monitoredOsProcList"])
            collLatency["monOsProcMetrics"] = time.time() - inicio
        if configDict["getRemoteOpen"]:
            inicio = time.time()
            from lib import metricremote as mr
            resposta["remoteOpenMetrics"] = mr.remote_open_exec.collect_remote_open(
                configDict["getRemoteOpen"], 
                configDict["remoteOpenList"])
            collLatency["remoteOpenMetrics"] = time.time() - inicio
        if configDict["getSelfIp"]:
            inicio = time.time()
            from lib import metricnet as mnet
            resposta["selfIpMetrics"] = mnet.net_exec.collect_selfip(
                configDict["getSelfIp"], 
                configDict["stationIpList"])
            collLatency["selfIpMetrics"] = time.time() - inicio
        if configDict["getSensor"]:
            inicio = time.time()
            from lib import metricsensor as sensor
            resposta["sensorMetrics"] = sensor.sensor_exec.collect_sensor(
                configDict["getSensor"])
            collLatency["sensorMetrics"] = time.time() - inicio
        if configDict["getServer"]:
            inicio = time.time()
            from lib import metricserver as srv
            resposta["serverMetrics"] = srv.server_exec.collect_server(
                configDict["getServer"])
            collLatency["serverMetrics"] = time.time() - inicio
        if configDict["getSysAgent"]:
            inicio = time.time()
            from lib import metricsysagent as sa
            resposta["sysAgentMetrics"] = sa.sys_agent_exec.collect_sys_agent(
                configDict["getSysAgent"], 
                configDict["sysAgentRestart"])
            collLatency["sysAgentMetrics"] = time.time() - inicio
        if configDict["getTopProcess"]:
            inicio = time.time()
            from lib import metrictop as mtop
            resposta["topMetrics"] = mtop.top_exec.collect_top(
                configDict["getTopProcess"], 
                configDict["topOsProcessCount"])
            collLatency["topMetrics"] = time.time() - inicio
        if configDict["getNetwork"]:
            net2 = mn.net_exec.get_net()
            netInterval = time.time() - net1start
            resposta["netMetrics"] = mn.net_exec.net_metrics(net1, net2, netInterval)
        if c.logFirstRun == 0: logging.info(
            f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-main.get_metrics: Latency info: {collLatency}")
        return resposta
        #----------------------------------------------------------------------------------------------------------------------
# Main 
if __name__ == "__main__":
    import time
    from lib import common as c
    from lib import metricconfig as mc
    from lib import pushtogateway as pg
    from lib import versioncontrol as vc
    c.versionDict["metric-collector"] = versao
    configDict = mc.config_setup.get_config()
    logging.basicConfig(filename = c.logPath + c.logFileName, level=logging.DEBUG, force=True)
    del mc
    while True:
        metrics = get_metrics(configDict)
        basic = pg.push_data(configDict, metrics)
        basic.set_data()
        basic.push_to_gateway()
        basic.clean_prom()
        # teste = vc.version_update.compare_versions(configDict)
        if not c.logFirstRun: logging.info(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-version dictionary: {c.versionDict}")
        c.logFirstRun = 1
        time.sleep(configDict["captureInterval"])
#######################################################################################################################
