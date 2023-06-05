#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#######################################################################################################################
versao = "metric-collector-v4.20-PUB-4d87eb0-20230508150250"
#######################################################################################################################
import logging 
#######################################################################################################################
# get metrics
def get_metrics(configDict):
        from lib import metricnet as mn
        resposta = {
            "bkpMetrics": 0,
            "camMetrics": 0,
            "diskMetrics": 0,
            "dockerMetrics": 0,
            "eyeflowDockerMetrics": 0,
            "gpuMetrics": 0,
            "lineMetrics": 0,
            "netMetrics": 0,
            "pingMetrics": 0,
            "processMetrics": 0,
            "topMetrics": 0,
            "selfIpMetrics": 0,
            "sensorMetrics": 0,
            "sysAgentMetrics": 0,
            "serverMetrics": 0}
        collLatency = {
            "bkpMetrics": 0,
            "camMetrics": 0,
            "diskMetrics": 0,
            "dockerMetrics": 0,
            "gpuMetrics": 0,
            "lineMetrics": 0,
            "pingMetrics": 0,
            "processMetrics": 0,
            "topMetrics": 0,
            "selfIpMetrics": 0,
            "sensorMetrics": 0,
            "sysAgentMetrics": 0,
            "serverMetrics": 0}
        net1 = mn.net_exec.get_net()
        net1start = time.time()
        if configDict["getBackup"]:
            inicio = time.time()
            from lib import metricbackup as bkp
            resposta["bkpMetrics"] = bkp.backup_exec.collect_backup(
                configDict["getBackup"], 
                configDict["backupFolder"], 
                configDict["backupFrequency"], 
                configDict["backupPrefix"], 
                configDict["backupSuffix"])
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
                configDict["eyeflowDocker"],
                configDict["eyeflowDockerExcept"])
            resposta["dockerMetrics"] = retorno["docker"]
            resposta["eyeflowDockerMetrics"] = retorno["eyeflow"]
            collLatency["dockerMetrics"] = time.time() - inicio
        if configDict["getGpuNvidia"]:
            inicio = time.time()
            from lib import metricgpu as gpu
            resposta["gpuMetrics"] = gpu.gpu_exec.collect_gpu(
                configDict["getGpuNvidia"])
            collLatency["gpuMetrics"] = time.time() - inicio
        if configDict["lineSensor"]:
            inicio = time.time()
            from lib import metricline as ml
            resposta["lineMetrics"] = ml.line_exec.collect_line(
                configDict["lineSensor"],
                configDict["lineSensrorUrl"])
            collLatency["lineMetrics"] = time.time() - inicio
        if configDict["getIpPing"]:
            inicio = time.time()
            from lib import metricping as ip
            resposta["pingMetrics"] = ip.ping_exec.collect_ping(
                configDict["getIpPing"], 
                configDict["pingList"])
            collLatency["pingMetrics"] = time.time() - inicio
        if configDict["getProcess"]:
            inicio = time.time()
            from lib import metricprocess as mp
            resposta["processMetrics"] = mp.process_exec.collect_process(
                configDict["getProcess"], 
                configDict["processNames"])
            collLatency["processMetrics"] = time.time() - inicio
        if configDict["getTopProcess"]:
            inicio = time.time()
            from lib import metrictop as mtop
            resposta["topMetrics"] = mtop.top_exec.collect_top(
                configDict["getTopProcess"], 
                configDict["topProcessNumber"])
            collLatency["topMetrics"] = time.time() - inicio
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
        if configDict["getSysAgent"]:
            inicio = time.time()
            from lib import metricsysagent as sa
            resposta["sysAgentMetrics"] = sa.sys_agent_exec.collect_sys_agent(
                configDict["getSysAgent"], 
                configDict["sysAgentRestart"])
            collLatency["sysAgentMetrics"] = time.time() - inicio
        if configDict["getServer"]:
            inicio = time.time()
            from lib import metricserver as srv
            resposta["serverMetrics"] = srv.server_exec.collect_server(
                configDict["getServer"])
            collLatency["serverMetrics"] = time.time() - inicio
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
    logging.basicConfig(filename = c.logPath + c.logFileName, level=logging.DEBUG)
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
