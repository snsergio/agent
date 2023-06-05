#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#######################################################################################################################
versao = "pushtogateway-v4.20-PUB-4d87eb0-20230508150250"
#######################################################################################################################
import logging
import time
from lib import common as c
#######################################################################################################################
c.versionDict["pushtogateway"] = versao
#######################################################################################################################
class push_data:
    # Set Prometheus registry
    def __init__(self, configDict, metricDict):
        from prometheus_client import CollectorRegistry, Gauge, Info
        if not c.logFirstRun: logging.info(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metriccam version: {versao}")
        self.registry = CollectorRegistry()
        self.configDict = configDict
        self.metricDict = metricDict
        if configDict["metricDetails"]:
            if configDict["getCam"] != 0:
                self.camSeq = Gauge("camera_sequence", "Camera frame sequence number", ["customer", "host", "camera"], registry=self.registry)
                self.camHeight = Gauge("camera_height", "Camera frame height", ["customer", "host", "camera"], registry=self.registry)
                self.camWidth = Gauge("camera_width", "Camera frame width", ["customer", "host", "camera"], registry=self.registry)
            if configDict["getDisk"]:
                self.diskSize = Gauge("disk_size", "Disk Size Bytes", ["customer", "host", "volume"], registry=self.registry)
                self.diskUsed = Gauge("disk_used", "Disk Used Bytes", ["customer", "host", "volume"], registry=self.registry)
            if configDict["getDocker"]:
                self.dockerPorts = Info("docker_ports", "Docker Image Ports Info", ["customer", "host", "image", "command", "names"], registry=self.registry)
            if configDict["getGpuNvidia"]:
                self.gpuMulti = Info("gpu_multi", "Multi-GPU Card", ["customer", "host", "card"], registry=self.registry)
                self.gpuState = Info("gpu_state", "GPU Performance State", ["customer", "host", "card"], registry=self.registry)
                self.gpuMode = Info("gpu_mode", "GPU Virtualization Mode", ["customer", "host", "card"], registry=self.registry)
                self.gpuBrand = Info("gpu_brand", "GPU Brand Information", ["customer", "host", "card"], registry=self.registry)
                self.gpuArch = Info("gpu_arch", "GPU Architecture Information", ["customer", "host", "card"], registry=self.registry)
                self.gpuDisplayMode = Info("gpu_display_mode", "GPU Display Mode", ["customer", "host", "card"], registry=self.registry)
                self.gpuDisplayActive = Info("gpu_display_active", "GPU Display Active Info", ["customer", "host", "card"], registry=self.registry)
            if configDict["getProcess"]:
                self.processTime = Gauge("process_time", "Running Process CPU time used (1/100s)", ["customer", "host", "process", "proccmd"], registry=self.registry)
                self.selfCpu = Gauge("self_cpu", "Monitoring Application CPU Utilization", ["customer", "host", "process", "proccmd"], registry=self.registry)
                self.selfMem = Gauge("self_mem", "Monitoring Application Memory Utilization", ["customer", "host", "process", "proccmd"], registry=self.registry)
            if configDict["getSensor"]:
                self.serverCoreV = Gauge("station_core_voltage", "Station CPU Core Voltage", ["customer", "host", "maxval"], registry=self.registry)
                self.server3v = Gauge("station_3v_voltage", "Station CPU 3.3v Voltage", ["customer", "host", "maxval"], registry=self.registry)
                self.server5v = Gauge("station_5v_voltage", "Station CPU 5v Voltage", ["customer", "host", "maxval"], registry=self.registry)
                self.server12v = Gauge("station_12v_voltage", "Station CPU 12v Voltage", ["customer", "host", "maxval"], registry=self.registry)
            if configDict["getSysAgent"]:
                self.sysagentPID = Gauge("sysagent_pid", "Sys Agent PID", ["customer", "host"], registry=self.registry)
                self.sysagentMem = Gauge("sysagent_memory", "Sys Agent memory allocated in MB", ["customer", "host"], registry=self.registry)
            if configDict["getServer"]:
                self.loadAvg1m = Gauge("station_load1m", "Station CPU Load Average 1 minute", ["customer", "host"], registry=self.registry)
                self.loadAvg5m = Gauge("station_load5m", "Station CPU Load Average 5 minutes", ["customer", "host"], registry=self.registry)
                self.loadAvg15m = Gauge("station_load15m", "Station CPU Load Average 15 minutes", ["customer", "host"], registry=self.registry)
                self.utilizationUser = Gauge("station_use_user", "Station CPU User Utilization", ["customer", "host"], registry=self.registry)
                self.utilizationSystem = Gauge("station_use_system", "Station CPU System Utilization", ["customer", "host"], registry=self.registry)
                self.taskTotal = Gauge("station_tasks_total", "Station CPU Tasks Total", ["customer", "host"], registry=self.registry)
                self.taskSleeping = Gauge("station_tasks_sleep", "Station CPU Tasks Sleeping", ["customer", "host"], registry=self.registry)
                self.taskZombie = Gauge("station_tasks_zombie", "Station CPU Tasks Zombie", ["customer", "host"], registry=self.registry)
        self.collectorVersion = Info("agent_version", "Collector Agent Version", ["customer", "host"], registry=self.registry)
        self.heartBeat = Gauge("station_heartbeat", "Station Heartbeat", ["customer", "host"], registry=self.registry)
        if configDict["getBackup"] != 0 and len(configDict["backupFolder"]) > 0:
            self.bkpStatus = Gauge("backup_status", "Check backup data returned no errors", ["customer", "host", "path", "name", "type"], registry=self.registry)
            self.bkpAccess = Gauge("backup_access", "Backup file last accessed", ["customer", "host", "path", "name", "type"], registry=self.registry)
            self.bkpModified = Gauge("backup_modified", "Backup file last modified", ["customer", "host", "path", "name", "type"], registry=self.registry)
            self.bkpAge = Gauge("backup_age", "Backup file age based on frequency", ["customer", "host", "path", "name", "type"], registry=self.registry)
        if configDict["getCam"] != 0 and len(configDict["camUrl"]) > 0:
            self.camStatus = Gauge("camera_status", "Camera status - 0 (off) / 1 (on)", ["customer", "host", "camera"], registry=self.registry)
            self.camHeartbeat = Gauge("camera_heartbeat", "Camera time - heartbeat", ["customer", "host", "camera"], registry=self.registry)
        if configDict["getDisk"]:
            self.diskUtilization = Gauge("disk_utilization", "Disk Utilization Percent", ["customer", "host", "volume"], registry=self.registry)
            self.diskRS = Gauge("disk_read_req_persec", "Disk Read Requests Completed per second", ["customer", "host", "device"], registry=self.registry)
            self.diskWS = Gauge("disk_write_req_persec", "Disk Write Requests Completed per second", ["customer", "host", "device"], registry=self.registry)
            self.diskRRQS = Gauge("disk_read_req_queued_persec", "Disk Read Requests per second Queued to the Device", ["customer", "host", "device"], registry=self.registry)
            self.diskWRQS = Gauge("disk_write_req_queued_persec", "Disk Write Requests per second Queued to the Device", ["customer", "host", "device"], registry=self.registry)
            self.diskRWait = Gauge("disk_read_await", "Disk Read Average Time (ms)", ["customer", "host", "device"], registry=self.registry)
            self.diskWWait = Gauge("disk_write_await", "Disk Write Average Time (ms)", ["customer", "host", "device"], registry=self.registry)
            self.diskAQL = Gauge("disk_avg_queue", "Disk Average Queue Length", ["customer", "host", "device"], registry=self.registry)
        if configDict["getDocker"]:
            self.dockerStatusInfo = Info("docker_status_info", "Docker Image Current Status", ["customer", "host", "image", "command", "names"], registry=self.registry)
            self.dockerStatus = Gauge("docker_status", "Docker Image Current Status", ["customer", "host", "image", "command", "names"], registry=self.registry)
            self.dockerStatusAge = Gauge("docker_status_age", "Docker Image Current Status Age", ["customer", "host", "image", "command", "names"], registry=self.registry)
            self.dockerCreated = Gauge("docker_created", "Docker Image Created Age", ["customer", "host", "image", "command", "names"], registry=self.registry)
            self.dockerEyeflowStatus = Gauge("docker_eyeflow_status", "Eyeflow Docker Image Current Status", ["customer", "host", "image", "command", "names", "efname"], registry=self.registry)
            self.dockerEyeflowAge = Gauge("docker_eyeflow_age", "Eyeflow Docker POD Running Time", ["customer", "host", "image", "command", "names", "efname"], registry=self.registry)
        if configDict["getGpuNvidia"]:
            self.gpuCuda = Info("gpu_cuda", "GPU CUDA Version", ["customer", "host", "card"], registry=self.registry)
            self.gpuDriver = Info("gpu_driver", "GPU Driver Version", ["customer", "host", "card"], registry=self.registry)
            self.gpuMemory = Gauge("gpu_memory", "GPU Memory Total", ["customer", "host", "card"], registry=self.registry)
            self.gpuMemUtilization = Gauge("gpu_mem_utilization", "GPU Memory Utilization Percent", ["customer", "host", "card"], registry=self.registry)
            self.gpuName = Info("gpu_name", "GPU Name", ["customer", "host", "card"], registry=self.registry)
            self.gpuPowerDraw = Gauge("gpu_power", "GPU Power Utilization Watts", ["customer", "host", "card"], registry=self.registry)
            self.gpuTemperature = Gauge("gpu_temperature", "GPU Temperature Celsius", ["customer", "host", "card"], registry=self.registry)
            self.gpuUtilization = Gauge("gpu_utilization", "GPU Utilization Percent", ["customer", "host", "card"], registry=self.registry)
            self.gpuFanPct = Gauge("gpu_fan_percent", "GPU Fan Speed Percent", ["customer", "host", "card"], registry=self.registry)
            self.gpuMemReserved = Gauge("gpu_mem_reserved", "GPU FB Memory Reserved", ["customer", "host", "card"], registry=self.registry)
            self.gpuMemUsed = Gauge("gpu_mem_used", "GPU FB Memory Used", ["customer", "host", "card"], registry=self.registry)
            self.gpuMemFree = Gauge("gpu_mem_free", "GPU FB Memory Free", ["customer", "host", "card"], registry=self.registry)
            self.gpuTempMax = Gauge("gpu_temp_max", "GPU Maximum Temperature", ["customer", "host", "card"], registry=self.registry)
            self.gpuTempSlow = Gauge("gpu_temp_slow", "GPU Slow Down Temperature", ["customer", "host", "card"], registry=self.registry)
            self.gpuTempTarget = Gauge("gpu_temp_target", "GPU Operating Target Temperature", ["customer", "host", "card"], registry=self.registry)
            self.gpuPowerLimit = Gauge("gpu_power_limit", "GPU Power Upper Limit", ["customer", "host", "card"], registry=self.registry)
            self.gpuPowerMax = Gauge("gpu_power_max", "GPU Maximum Power", ["customer", "host", "card"], registry=self.registry)
        if configDict["lineSensor"]:
            self.lineSensorResponse = Gauge("response", "Line Sensor URL response", ["customer", "host", "url"], registry=self.registry)
            self.lineSensorStatus = Info("status", "Line Sensor GET response", ["customer", "host", "url"], registry=self.registry)
        if configDict["getNetwork"]:
            self.networkIP = Info("nic_ip", "NIC Card IP Address", ["customer", "host", "nic"], registry=self.registry)
            self.networkRx = Gauge("nic_rx", "NIC Card UP receiving bytes per second", ["customer", "host", "nic"], registry=self.registry)
            self.networkTx = Gauge("nic_tx", "NIC Card UP transmiting bytes per second", ["customer", "host", "nic"], registry=self.registry)
        if configDict["getIpPing"] and configDict["pingList"] != 0:
            self.pingtime = Gauge("ping_exec_time", "Ping time execution", ["customer", "host", "ipaddr"], registry=self.registry)
            self.pingLoss = Gauge("ping_loss_pct", "Ping loss percentage", ["customer", "host", "ipaddr"], registry=self.registry)
        if configDict["getProcess"]:
            self.processCPU = Gauge("process_cpu", "Running Process CPU Usage", ["customer", "host", "process", "proccmd"], registry=self.registry)
            self.processMEM = Gauge("process_mem", "Running Process Memory Usage", ["customer", "host", "process", "proccmd"], registry=self.registry)
            self.processPID = Gauge("process_pid", "Running Process PID", ["customer", "host", "process", "proccmd"], registry=self.registry)
            self.processActive = Gauge("process_active", "Selected Processes Running Status", ["customer", "host", "process", "proccmd"], registry=self.registry)
            self.processMissing = Gauge("process_missing", "Selected Processes Running Status", ["customer", "host", "process"], registry=self.registry)
        if configDict["getTopProcess"]:
            self.topProcCPU = Gauge("top_process_cpu", "Running Top Offender Process CPU Usage", ["customer", "host", "rank", "filter"], registry=self.registry)
            self.topProcMEM = Gauge("top_process_mem", "Running Top Offender Process Memory Usage", ["customer", "host", "rank", "filter"], registry=self.registry)
            self.topProcPID = Gauge("top_process_pid", "Running Top Offender Process PID", ["customer", "host", "rank", "filter"], registry=self.registry)
            self.topProcName = Info("top_process_name", "Running Top Offender Process Name", ["customer", "host", "rank", "filter"], registry=self.registry)
        if configDict["getSelfIp"] and configDict["stationIpList"] != 0:
            self.selfIpPresent = Gauge("selfip_exec_time", "Ping time execution", ["customer", "host", "ipaddr"], registry=self.registry)
        if configDict["getSensor"]:
            self.serverChassisFan = Gauge("station_chassis_fan", "Station Chassis Fan RPM", ["customer", "host", "maxval"], registry=self.registry)
            self.serverCpuFan = Gauge("station_cpu_fan", "Station CPU Fan RPM", ["customer", "host", "maxval"], registry=self.registry)
            self.serverPciPower = Gauge("station_pci_power", "Station PCI Power", ["customer", "host", "maxval"], registry=self.registry)
            self.serverCpuTemp = Gauge("station_cpu_temp", "Station CPU Temperature", ["customer", "host", "maxval"], registry=self.registry)
            self.serverMbTemp = Gauge("station_mb_temp", "Station Motherboard Temperature", ["customer", "host", "maxval"], registry=self.registry)
            self.serverPciTemp = Gauge("station_pci_temp", "Station PCI Temperature", ["customer", "host", "maxval"], registry=self.registry)
        if configDict["getSysAgent"]:
            self.sysagentLoaded = Gauge("sysagent_loaded", "Sys Agent is loaded as a service", ["customer", "host"], registry=self.registry)
            self.sysagentActive = Gauge("sysagent_active", "Sys Agent is active", ["customer", "host"], registry=self.registry)
            self.sysagentError = Gauge("sysagent_error", "Sys Agent has errors", ["customer", "host"], registry=self.registry)
        if configDict["getServer"]:
            self.serverCores = Gauge("station_cores", "Station CPU Cores", ["customer", "host"], registry=self.registry)
            self.serverMemFree = Gauge("station_mem_free", "Station Memory Free", ["customer", "host"], registry=self.registry)
            self.serverMemCached = Gauge("station_mem_cached", "Station Memory Cached", ["customer", "host"], registry=self.registry)
            self.serverMemTotal = Gauge("station_mem_total", "Station Memory Total", ["customer", "host"], registry=self.registry)
            self.serverMemUsed = Gauge("station_mem_used", "Station Memory Used", ["customer", "host"], registry=self.registry)
            self.serverUptime = Info("station_uptime", "Station Uptime", ["customer", "host"], registry=self.registry)
            self.serverTimeStamp = Info("station_timestamp", "Station Timestamp", ["customer", "host"], registry=self.registry)
            self.taskRunning = Gauge("station_tasks_running", "Station CPU Tasks Running", ["customer", "host"], registry=self.registry)
            self.taskStopped = Gauge("station_tasks_stop", "Station CPU Tasks Stopped", ["customer", "host"], registry=self.registry)
            self.utilizationIdle = Gauge("station_use_idle", "Station CPU Idle", ["customer", "host"], registry=self.registry)
        return
        #----------------------------------------------------------------------------------------------------------------------
    def clean_prom(self):
        if self.configDict["metricDetails"]:
            if self.configDict["getCam"] and self.configDict["camUrl"] != 0:
                self.camSeq.clear()
                self.camHeight.clear()
                self.camWidth.clear()
            if self.configDict["getDisk"]:
                self.diskSize.clear()
                self.diskUsed.clear()
            if self.configDict["getDocker"]:
                self.dockerPorts.clear()
            if self.configDict["getGpuNvidia"]:
                self.gpuMulti.clear()
                self.gpuState.clear()
                self.gpuMode.clear()
                self.gpuBrand.clear()
                self.gpuArch.clear()
                self.gpuDisplayMode.clear()
                self.gpuDisplayActive.clear()
            if self.configDict["getProcess"]:
                self.processTime.clear()
                self.selfCpu.clear()
                self.selfMem.clear()
            if self.configDict["getSensor"]:
                self.serverCoreV.clear()
                self.server3v.clear()
                self.server5v.clear()
                self.server12v.clear()
            if self.configDict["getSysAgent"]:
                self.sysagentPID.clear()
                self.sysagentMem.clear()
            if self.configDict["getServer"]:
                self.loadAvg1m.clear()
                self.loadAvg5m.clear()
                self.loadAvg15m.clear()
                self.utilizationUser.clear()
                self.utilizationSystem.clear()
                self.taskTotal.clear()
                self.taskSleeping.clear()
                self.taskZombie.clear()
        self.collectorVersion.clear()
        self.heartBeat.clear()
        if self.configDict["getBackup"] != 0 and len(self.configDict["backupFolder"]) > 0:
            self.bkpStatus.clear()
            self.bkpAccess.clear()
            self.bkpModified.clear()
            self.bkpAge.clear()
        if self.configDict["getCam"] and self.configDict["camUrl"] != 0:
            self.camStatus.clear()
            self.camHeartbeat.clear()
        if self.configDict["getDisk"]:
            self.diskUtilization.clear()
            self.diskRS.clear()
            self.diskWS.clear()
            self.diskRRQS.clear()
            self.diskWRQS.clear()
            self.diskRWait.clear()
            self.diskWWait.clear()
            self.diskAQL.clear()
        if self.configDict["getDocker"]:
            self.dockerStatusInfo.clear()
            self.dockerStatus.clear()
            self.dockerStatusAge.clear()
            self.dockerCreated.clear()
            self.dockerEyeflowStatus.clear()
            self.dockerEyeflowAge.clear()
        if self.configDict["getGpuNvidia"]:
            self.gpuCuda.clear()
            self.gpuDriver.clear()
            self.gpuMemory.clear()
            self.gpuMemUtilization.clear()
            self.gpuName.clear()
            self.gpuPowerDraw.clear()
            self.gpuTemperature.clear()
            self.gpuUtilization.clear()
            self.gpuFanPct.clear()
            self.gpuMemReserved.clear()
            self.gpuMemUsed.clear()
            self.gpuMemFree.clear()
            self.gpuTempMax.clear()
            self.gpuTempSlow.clear()
            self.gpuTempTarget.clear()
            self.gpuPowerLimit.clear()
            self.gpuPowerMax.clear()
        if self.configDict["lineSensor"]:
            self.lineSensorResponse.clear()
            self.lineSensorStatus.clear()
        if self.configDict["getNetwork"]:
            self.networkIP.clear()
            self.networkRx.clear()
            self.networkTx.clear()
        if self.configDict["getIpPing"] and self.configDict["pingList"] != 0:
            self.pingtime.clear()
            self.pingLoss.clear()
        if self.configDict["getProcess"]:
            self.processCPU.clear()
            self.processMEM.clear()
            self.processPID.clear()
            self.processActive.clear()
            self.processMissing.clear()
        if self.configDict["getTopProcess"]:
            self.topProcCPU.clear()
            self.topProcMEM.clear()
            self.topProcPID.clear()
            self.topProcName.clear()
        if self.configDict["getSelfIp"] and self.configDict["stationIpList"] != 0:
            self.selfIpPresent.clear()
        if self.configDict["getSensor"]:
            self.serverChassisFan.clear()
            self.serverCpuFan.clear()
            self.serverPciPower.clear()
            self.serverCpuTemp.clear()
            self.serverMbTemp.clear()
            self.serverPciTemp.clear()
        if self.configDict["getSysAgent"]:
            self.sysagentLoaded.clear()
            self.sysagentActive.clear()
            self.sysagentError.clear()
        if self.configDict["getServer"]:
            self.serverCores.clear()
            self.serverMemFree.clear()
            self.serverMemCached.clear()
            self.serverMemTotal.clear()
            self.serverMemUsed.clear()
            self.serverUptime.clear()
            self.serverTimeStamp.clear()
            self.taskRunning.clear()
            self.taskStopped.clear()
            self.utilizationIdle.clear()
        return
        #----------------------------------------------------------------------------------------------------------------------
    def set_data(self):
        self.collectorVersion.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"]).info({"agent_version": versao})
        self.heartBeat.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"]).set(time.time())
        if self.configDict["metricDetails"]:
            if self.configDict["getGpuNvidia"] and self.metricDict["gpuMetrics"] != 0:
                self.gpuMulti.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).info({"gpu_multi": self.metricDict["gpuMetrics"]["multiGpu"]})
                self.gpuState.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).info({"gpu_state": self.metricDict["gpuMetrics"]["performanceState"]})
                self.gpuMode.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).info({"gpu_mode": self.metricDict["gpuMetrics"]["virtMode"]})
                self.gpuBrand.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).info({"gpu_brand": self.metricDict["gpuMetrics"]["gpuBrand"]})
                self.gpuArch.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).info({"gpu_arch": self.metricDict["gpuMetrics"]["gpuArch"]})
                self.gpuDisplayMode.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).info({"gpu_display_mode": self.metricDict["gpuMetrics"]["gpuDisplayMode"]})
                self.gpuDisplayActive.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).info({"gpu_display_active": self.metricDict["gpuMetrics"]["gpuDisplayActive"]})
            if self.configDict["getSensor"] and self.metricDict["sensorMetrics"] != 0:
                self.serverCoreV.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], maxval=self.metricDict["sensorMetrics"]["vCoreMax"]).set(self.metricDict["sensorMetrics"]["vCore"])
                self.server3v.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], maxval=self.metricDict["sensorMetrics"]["v3.3Max"]).set(self.metricDict["sensorMetrics"]["v3.3"])
                self.server5v.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], maxval=self.metricDict["sensorMetrics"]["v5.0Max"]).set(self.metricDict["sensorMetrics"]["v5.0"])
                self.server12v.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], maxval=self.metricDict["sensorMetrics"]["v12.0Max"]).set(self.metricDict["sensorMetrics"]["v12.0"])
            if self.configDict["getServer"] and self.metricDict["serverMetrics"] != 0:
                self.loadAvg1m.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"]).set(self.metricDict["serverMetrics"]["loadAvg1m"])
                self.loadAvg5m.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"]).set(self.metricDict["serverMetrics"]["loadAvg5m"])
                self.loadAvg15m.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"]).set(self.metricDict["serverMetrics"]["loadAvg15m"])
                self.utilizationUser.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"]).set(self.metricDict["serverMetrics"]["cpuUser"])
                self.utilizationSystem.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"]).set(self.metricDict["serverMetrics"]["cpuSys"])
                self.taskTotal.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"]).set(self.metricDict["serverMetrics"]["taskTotal"])
                self.taskSleeping.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"]).set(self.metricDict["serverMetrics"]["taskSleeping"])
                self.taskZombie.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"]).set(self.metricDict["serverMetrics"]["taskZombie"])
        if self.configDict["getBackup"] != 0 and self.metricDict["bkpMetrics"] and len(self.configDict["backupFolder"]) > 0:
            for element in range(len(self.metricDict["bkpMetrics"])):
                self.bkpStatus.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], path=self.metricDict["bkpMetrics"][element]["path"], name=self.metricDict["bkpMetrics"][element]["name"], type=self.metricDict["bkpMetrics"][element]["type"]).set(self.metricDict["bkpMetrics"][element]["status"])
                self.bkpAccess.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], path=self.metricDict["bkpMetrics"][element]["path"], name=self.metricDict["bkpMetrics"][element]["name"], type=self.metricDict["bkpMetrics"][element]["type"]).set(self.metricDict["bkpMetrics"][element]["access"])
                self.bkpModified.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], path=self.metricDict["bkpMetrics"][element]["path"], name=self.metricDict["bkpMetrics"][element]["name"], type=self.metricDict["bkpMetrics"][element]["type"]).set(self.metricDict["bkpMetrics"][element]["modified"])
                self.bkpAge.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], path=self.metricDict["bkpMetrics"][element]["path"], name=self.metricDict["bkpMetrics"][element]["name"], type=self.metricDict["bkpMetrics"][element]["type"]).set(self.metricDict["bkpMetrics"][element]["age"])
        if self.configDict["getCam"] and self.configDict["camUrl"] != 0 and self.metricDict["camMetrics"] != 0:
            for element in range(len(self.metricDict["camMetrics"])):
                self.camStatus.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], camera=self.metricDict["camMetrics"][element]["camName"]).set(self.metricDict["camMetrics"][element]["status"])
                if self.configDict["metricDetails"]: self.camSeq.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], camera=self.metricDict["camMetrics"][element]["camName"]).set(self.metricDict["camMetrics"][element]["frameSeq"])
                self.camHeartbeat.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], camera=self.metricDict["camMetrics"][element]["camName"]).set(self.metricDict["camMetrics"][element]["camHB"])
                if self.configDict["metricDetails"]: self.camHeight.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], camera=self.metricDict["camMetrics"][element]["camName"]).set(self.metricDict["camMetrics"][element]["camHeight"])
                if self.configDict["metricDetails"]: self.camWidth.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], camera=self.metricDict["camMetrics"][element]["camName"]).set(self.metricDict["camMetrics"][element]["camWidth"])
        if self.configDict["getDisk"] and self.metricDict["diskMetrics"] != 0:
            for element in range(len(self.metricDict["diskMetrics"])):
                if "volume" in self.metricDict["diskMetrics"][element].keys():
                    self.diskUtilization.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], volume=self.metricDict["diskMetrics"][element]["volume"]).set(self.metricDict["diskMetrics"][element]["usedPct"])
                    if self.configDict["metricDetails"]:
                        self.diskSize.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], volume=self.metricDict["diskMetrics"][element]["volume"]).set(self.metricDict["diskMetrics"][element]["size"])
                        self.diskUsed.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], volume=self.metricDict["diskMetrics"][element]["volume"]).set(self.metricDict["diskMetrics"][element]["used"])
                elif "device" in self.metricDict["diskMetrics"][element].keys():
                    self.diskRS.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], device=self.metricDict["diskMetrics"][element]["device"]).set(self.metricDict["diskMetrics"][element]["rrps"])
                    self.diskWS.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], device=self.metricDict["diskMetrics"][element]["device"]).set(self.metricDict["diskMetrics"][element]["wrps"])
                    self.diskRRQS.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], device=self.metricDict["diskMetrics"][element]["device"]).set(self.metricDict["diskMetrics"][element]["rrqps"])
                    self.diskWRQS.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], device=self.metricDict["diskMetrics"][element]["device"]).set(self.metricDict["diskMetrics"][element]["wrqps"])
                    self.diskRWait.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], device=self.metricDict["diskMetrics"][element]["device"]).set(self.metricDict["diskMetrics"][element]["rawait"])
                    self.diskWWait.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], device=self.metricDict["diskMetrics"][element]["device"]).set(self.metricDict["diskMetrics"][element]["wawait"])
                    self.diskAQL.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], device=self.metricDict["diskMetrics"][element]["device"]).set(self.metricDict["diskMetrics"][element]["aql"])
        if self.configDict["getDocker"] and self.metricDict["dockerMetrics"] != 0:
            for element in range(len(self.metricDict["dockerMetrics"])):
                imageInfo = self.metricDict["dockerMetrics"][element]["image"]
                portsInfo = self.metricDict["dockerMetrics"][element]["ports"]
                statusInfo = self.metricDict["dockerMetrics"][element]["status"]
                if statusInfo == "up": statusGauge = 1
                else: statusGauge = 0
                if self.configDict["metricDetails"]: self.dockerPorts.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], image=imageInfo, command=self.metricDict["dockerMetrics"][element]["command"], names=self.metricDict["dockerMetrics"][element]["names"]).info({"docker_ports": portsInfo})
                self.dockerStatusInfo.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], image=imageInfo, command=self.metricDict["dockerMetrics"][element]["command"], names=self.metricDict["dockerMetrics"][element]["names"]).info({"docker_status_info": statusInfo})
                self.dockerStatus.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], image=imageInfo, command=self.metricDict["dockerMetrics"][element]["command"], names=self.metricDict["dockerMetrics"][element]["names"]).set(statusGauge)
                self.dockerStatusAge.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], image=imageInfo, command=self.metricDict["dockerMetrics"][element]["command"], names=self.metricDict["dockerMetrics"][element]["names"]).set(self.metricDict["dockerMetrics"][element]["statusTime"])
                self.dockerCreated.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], image=imageInfo, command=self.metricDict["dockerMetrics"][element]["command"], names=self.metricDict["dockerMetrics"][element]["names"]).set(self.metricDict["dockerMetrics"][element]["created"])
            if self.metricDict["eyeflowDockerMetrics"] != 0:
                for element in range(len(self.metricDict["eyeflowDockerMetrics"])):
                    if statusInfo == "up": statusGauge = 1
                    else: statusGauge = 0
                    self.dockerEyeflowStatus.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], image=self.metricDict["eyeflowDockerMetrics"][element]["image"], command=self.metricDict["eyeflowDockerMetrics"][element]["command"], names=self.metricDict["eyeflowDockerMetrics"][element]["names"], efname=self.metricDict["eyeflowDockerMetrics"][element]["efname"]).set(statusGauge)
                    self.dockerEyeflowAge.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], image=self.metricDict["eyeflowDockerMetrics"][element]["image"], command=self.metricDict["eyeflowDockerMetrics"][element]["command"], names=self.metricDict["eyeflowDockerMetrics"][element]["names"], efname=self.metricDict["eyeflowDockerMetrics"][element]["efname"]).set(self.metricDict["eyeflowDockerMetrics"][element]["created"])
        if self.configDict["getGpuNvidia"] and self.metricDict["gpuMetrics"] != 0:
            self.gpuCuda.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).info({"gpu_cuda": self.metricDict["gpuMetrics"]["cuda"]})
            self.gpuDriver.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).info({"gpu_driver": self.metricDict["gpuMetrics"]["driver"]})
            self.gpuMemory.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).set(self.metricDict["gpuMetrics"]["memTotal"])
            self.gpuMemUtilization.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).set(self.metricDict["gpuMetrics"]["memUtil"])
            self.gpuName.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).info({"gpu_name": self.metricDict["gpuMetrics"]["gpuName"]})
            self.gpuPowerDraw.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).set(self.metricDict["gpuMetrics"]["powerDraw"])
            self.gpuTemperature.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).set(self.metricDict["gpuMetrics"]["temperature"])
            self.gpuUtilization.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).set(self.metricDict["gpuMetrics"]["gpuUtil"])
            self.gpuFanPct.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).set(self.metricDict["gpuMetrics"]["fanSpeed"])
            self.gpuMemReserved.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).set(self.metricDict["gpuMetrics"]["memReserved"])
            self.gpuMemUsed.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).set(self.metricDict["gpuMetrics"]["memUsed"])
            self.gpuMemFree.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).set(self.metricDict["gpuMetrics"]["memFree"])
            self.gpuTempMax.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).set(self.metricDict["gpuMetrics"]["tempMax"])
            self.gpuTempSlow.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).set(self.metricDict["gpuMetrics"]["tempSlowDn"])
            self.gpuTempTarget.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).set(self.metricDict["gpuMetrics"]["tempTarget"])
            self.gpuPowerLimit.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).set(self.metricDict["gpuMetrics"]["powerLimit"])
            self.gpuPowerMax.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).set(self.metricDict["gpuMetrics"]["powerMax"])
        if self.configDict["lineSensor"] and self.metricDict["lineMetrics"] != 0:
            for element in range(len(self.metricDict["lineMetrics"])):
                self.lineSensorResponse.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], url=self.metricDict["lineMetrics"][element]["lineSensorUrl"]).set(int(self.metricDict["lineMetrics"][element]["lineSensorStatus"]))
                self.lineSensorStatus.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], url=self.metricDict["lineMetrics"][element]["lineSensorUrl"]).info({"response": self.metricDict["lineMetrics"][element]["lineSensorResponse"]})
        if self.configDict["getNetwork"] and self.metricDict["netMetrics"] != 0:
            for element in range(len(self.metricDict["netMetrics"])):
                self.networkIP.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], nic=self.metricDict["netMetrics"][element]["name"]).info({"ip": self.metricDict["netMetrics"][element]["ipAddr"]})
                self.networkRx.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], nic=self.metricDict["netMetrics"][element]["name"]).set(self.metricDict["netMetrics"][element]["rxBps"])
                self.networkTx.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], nic=self.metricDict["netMetrics"][element]["name"]).set(self.metricDict["netMetrics"][element]["txBps"])
        if self.configDict["getIpPing"] and self.configDict["pingList"] != 0:
            for item in range(len(self.metricDict["pingMetrics"])):
                self.pingtime.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], ipaddr=self.metricDict["pingMetrics"][item]["ipAddr"].strip()).set(self.metricDict["pingMetrics"][item]["resp"]["execTime"])
                self.pingLoss.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], ipaddr=self.metricDict["pingMetrics"][item]["ipAddr"].strip()).set(self.metricDict["pingMetrics"][item]["resp"]["packLoss"])
        if self.configDict["getProcess"] and self.metricDict["processMetrics"] != 0:
            for element in range(len(self.metricDict["processMetrics"]) - 1):
                self.processCPU.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], process=self.metricDict["processMetrics"][element]["processCfg"], proccmd=self.metricDict["processMetrics"][element]["cmd"]).set(self.metricDict["processMetrics"][element]["cpu"])
                self.processMEM.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], process=self.metricDict["processMetrics"][element]["processCfg"], proccmd=self.metricDict["processMetrics"][element]["cmd"]).set(self.metricDict["processMetrics"][element]["mem"])
                self.processPID.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], process=self.metricDict["processMetrics"][element]["processCfg"], proccmd=self.metricDict["processMetrics"][element]["cmd"]).set(self.metricDict["processMetrics"][element]["pid"])
                self.processActive.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], process=self.metricDict["processMetrics"][element]["processCfg"], proccmd=self.metricDict["processMetrics"][element]["cmd"]).set(self.metricDict["processMetrics"][element]["processActive"])
                if self.configDict["metricDetails"]:
                    self.processTime.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], process=self.metricDict["processMetrics"][element]["processCfg"], proccmd=self.metricDict["processMetrics"][element]["cmd"]).set(self.metricDict["processMetrics"][element]["time"])
                    self.selfCpu.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], process=self.metricDict["processMetrics"][element]["processCfg"], proccmd=self.metricDict["processMetrics"][element]["cmd"]).set(self.metricDict["serverMetrics"]["selfCpuUsage"])
                    self.selfMem.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], process=self.metricDict["processMetrics"][element]["processCfg"], proccmd=self.metricDict["processMetrics"][element]["cmd"]).set(self.metricDict["serverMetrics"]["selfMemUsage"])
            self.processMissing.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], process=self.metricDict["processMetrics"][element]["processCfg"]).set(len(self.metricDict["processMetrics"]["missingProcess"]))
        if self.configDict["getTopProcess"]:
            for element in range(len(self.metricDict["topMetrics"])):
                self.topProcCPU.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], rank=self.metricDict["topMetrics"][element]["rank"], filter=str(self.metricDict["topMetrics"][element]["rank"])+"-"+self.configDict["hostName"]).set(self.metricDict["topMetrics"][element]["cpu"])
                self.topProcMEM.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], rank=self.metricDict["topMetrics"][element]["rank"], filter=str(self.metricDict["topMetrics"][element]["rank"])+"-"+self.configDict["hostName"]).set(self.metricDict["topMetrics"][element]["mem"])
                self.topProcPID.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], rank=self.metricDict["topMetrics"][element]["rank"], filter=str(self.metricDict["topMetrics"][element]["rank"])+"-"+self.configDict["hostName"]).set(self.metricDict["topMetrics"][element]["pid"])
                self.topProcName.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], rank=self.metricDict["topMetrics"][element]["rank"], filter=str(self.metricDict["topMetrics"][element]["rank"])+"-"+self.configDict["hostName"]).info({"top_process_name": self.metricDict["topMetrics"][element]["cmd"]})
        if self.configDict["getSelfIp"] and self.metricDict["selfIpMetrics"] != 0:
            for element in self.metricDict["selfIpMetrics"].keys():
                self.selfIpPresent.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], ipaddr=element).set(self.metricDict["selfIpMetrics"][element])
        if self.configDict["getSensor"] and self.metricDict["sensorMetrics"] != 0:
            self.serverChassisFan.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], maxval=self.metricDict["sensorMetrics"]["chassisFanRpmMax"]).set(self.metricDict["sensorMetrics"]["chassisFanRPM"])
            self.serverCpuFan.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], maxval=self.metricDict["sensorMetrics"]["cpuFanRpmMax"]).set(self.metricDict["sensorMetrics"]["cpuFanRPM"])
            self.serverPciPower.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], maxval=self.metricDict["sensorMetrics"]["pciPowerMax"]).set(self.metricDict["sensorMetrics"]["pciPower"])
            self.serverCpuTemp.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], maxval=self.metricDict["sensorMetrics"]["cpuTempMax"]).set(self.metricDict["sensorMetrics"]["cpuTemp"])
            self.serverMbTemp.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], maxval=self.metricDict["sensorMetrics"]["mbTempMax"]).set(self.metricDict["sensorMetrics"]["mbTemp"])
            self.serverPciTemp.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"], maxval=self.metricDict["sensorMetrics"]["pciTempMax"]).set(self.metricDict["sensorMetrics"]["pciTemp"])
        if self.configDict["getSysAgent"] and self.metricDict["sysAgentMetrics"] != 0:
            if self.metricDict["sysAgentMetrics"]["saLoaded"] == "loaded": saL = 1
            else: saL = 0
            if self.metricDict["sysAgentMetrics"]["saActive"] == "active": saA = 1
            else: saA = 0
            if self.configDict["metricDetails"]: self.sysagentPID.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"]).set(self.metricDict["sysAgentMetrics"]["saPID"])
            if self.configDict["metricDetails"]: self.sysagentMem.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"]).set(self.metricDict["sysAgentMetrics"]["saMEM"])
            self.sysagentLoaded.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"]).set(saL)
            self.sysagentActive.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"]).set(saA)
            self.sysagentError.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"]).set(self.metricDict["sysAgentMetrics"]["saError"])
        if self.configDict["getServer"] and self.metricDict["serverMetrics"] != 0:
            self.serverCores.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"]).set(self.metricDict["serverMetrics"]["cpuCores"])
            self.serverMemFree.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"]).set(self.metricDict["serverMetrics"]["memFree"])
            self.serverMemCached.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"]).set(self.metricDict["serverMetrics"]["memCached"])
            self.serverMemTotal.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"]).set(self.metricDict["serverMetrics"]["memTotal"])
            self.serverMemUsed.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"]).set(self.metricDict["serverMetrics"]["memUsed"])
            self.serverUptime.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"]).info({"station_uptime": self.metricDict["serverMetrics"]["serverUp"]})
            self.serverTimeStamp.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"]).info({"station_timestamp": self.metricDict["serverMetrics"]["servertime"]})
            self.taskRunning.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"]).set(self.metricDict["serverMetrics"]["taskRunning"])
            self.taskStopped.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"]).set(self.metricDict["serverMetrics"]["taskStopped"])
            self.utilizationIdle.labels(customer=self.configDict["customerName"], host=self.configDict["hostName"]).set(self.metricDict["serverMetrics"]["cpuIdle"])
        return
        #----------------------------------------------------------------------------------------------------------------------
    def push_to_gateway(self):
        from prometheus_client import push_to_gateway
        from prometheus_client.exposition import basic_auth_handler
        user1 = self.configDict["user1"]
        pass1 = self.configDict["pass1"]
        user2 = self.configDict["user2"]
        pass2 = self.configDict["pass2"]
        def auth_handler(url, method, timeout, headers, data):
            return basic_auth_handler(url, method, timeout, headers, data, user1, pass1)
        def auth_handler_2(url, method, timeout, headers, data):
            return basic_auth_handler(url, method, timeout, headers, data, user2, pass2)
        if self.configDict["pushUrl"] not in [None, ""]:
            if self.configDict["tls1"]:
                iref = "https"
                if self.configDict["pushUrl"].split(":")[0] == "http": self.configDict["pushUrl"] = iref+self.configDict["pushUrl"].split(":")[1]
                elif self.configDict["pushUrl"].split(":")[0] == "https": pass
                else: self.configDict["pushUrl"] = iref+"://"+self.configDict["pushUrl"]
                try: push_to_gateway(self.configDict["pushUrl"], job=self.configDict["customerName"], registry=self.registry, handler=auth_handler)
                except: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-push_data.push_to_gateway: Push to TLS Gateway error")
            else:
                iref = "http"
                if self.configDict["pushUrl"].split(":")[0] == "https": self.configDict["pushUrl"] = iref+self.configDict["pushUrl"].split(":")[1]
                elif self.configDict["pushUrl"].split(":")[0] == "http": pass
                else: self.configDict["pushUrl"] = iref+"://"+self.configDict["pushUrl"]
                try: push_to_gateway(self.configDict["pushUrl"], job=self.configDict["customerName"], registry=self.registry)
                except: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-push_data.push_to_gateway: Push to http Gateway error")
            if self.configDict["debugMode"]: logging.debug(f"[DEBUG] {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-Push Metrics: PushURL: {self.configDict['pushUrl']}, Job: {self.configDict['customerName']}")
        if self.configDict["pushUrl2"] not in [None, ""]:
            if self.configDict["tls2"]:
                iref = "https"
                if self.configDict["pushUrl2"].split(":")[0] == "http": self.configDict["pushUrl2"] = iref+self.configDict["pushUrl2"].split(":")[1]
                elif self.configDict["pushUrl2"].split(":")[0] == "https": pass
                else: self.configDict["pushUrl2"] = iref+"://"+self.configDict["pushUrl2"]
                try: push_to_gateway(self.configDict["pushUrl2"], job=self.configDict["customerName"], registry=self.registry, handler=auth_handler_2)
                except: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-push_data.push_to_gateway: Push to TLS Gateway 2 error")
            else:
                iref = "http"
                if self.configDict["pushUrl2"].split(":")[0] == "https": self.configDict["pushUrl2"] = iref+self.configDict["pushUrl2"].split(":")[1]
                elif self.configDict["pushUrl2"].split(":")[0] == "http": pass
                else: self.configDict["pushUrl2"] = iref+"://"+self.configDict["pushUrl2"]
                try: push_to_gateway(self.configDict["pushUrl2"], job=self.configDict["customerName"], registry=self.registry, handler=auth_handler_2)
                except: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-Push Metrics: Push to http Gateway 2 error")
            if self.configDict["debugMode"]: logging.debug(f"[DEBUG] {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-Push Metrics: PushURL2: {self.configDict['pushUrl2']}, Job: {self.configDict['customerName']}")
        return
        #----------------------------------------------------------------------------------------------------------------------
