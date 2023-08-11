#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#######################################################################################################################
versao = "metricexporter-v5.11-PUB-c26a2db-20230811163629"
#######################################################################################################################
import logging
import time
from prometheus_client.core import Gauge, Info
from lib import common as c
#######################################################################################################################
c.versionDict["metricexporter"] = versao
#######################################################################################################################
class exporter(object): 
    # Set Prometheus registry
    def __init__(self, configDict):
        if not c.logFirstRun: logging.info(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metriccam version: {versao}")
        self.configDict = configDict
        self.metricDict = {}
        # Metric API Get
        if configDict["getApiGet"] == 2:
            self.apiGetUrl = Info("api_get_url", "API GET response - URL", ["customer", "station", "host"])
        if configDict["getApiGet"] >= 1:
            self.apiGetExecError = Gauge("error_exec_api_get", "API GET - Command Execution Error", ["customer", "station", "host", "mod"])
            self.apiGetExists = Gauge("api_get_exists", "API GET - endpoint exists", ["customer", "station", "host", "url"])
            self.apiGetStatus = Gauge("api_get_status", "API GET - endpoint status", ["customer", "station", "host", "url"])
            self.apiGetResponse = Info("api_get_response", "API GET - endpoint response", ["customer", "station", "host", "url"])
        # Metric Backup
        if configDict["getBackup"] >= 1:
            self.bkpExecError = Gauge("error_exec_backup", "Backup - Command Execution Error", ["customer", "station", "host", "mod"])
            self.bkpStatus = Gauge("backup_status", "Check backup data returned no errors", ["customer", "station", "host", "path", "name", "join"])
            self.bkpAccess = Gauge("backup_access", "Backup file last accessed", ["customer", "station", "host", "path", "name", "join"])
            self.bkpModified = Gauge("backup_modified", "Backup file last modified", ["customer", "station", "host", "path", "name", "join"])
            self.bkpExpire = Gauge("backup_expire", "Backup file age based on frequency", ["customer", "station", "host", "path", "name", "join"])
        # Metric Cam
        if configDict["getCam"] == 2:
            self.camSeq = Gauge("camera_sequence", "Camera frame sequence number", ["customer", "station", "host", "camera", "url", "endpoint"])
            self.camHeight = Gauge("camera_height", "Camera frame height", ["customer", "station", "host", "camera", "url", "endpoint"])
            self.camWidth = Gauge("camera_width", "Camera frame width", ["customer", "station", "host", "camera", "url", "endpoint"])
        if configDict["getCam"] >= 1:
            self.camExecError = Gauge("error_exec_camera", "Camera API - Command Execution Error", ["customer", "station", "host", "mod"])
            self.camRestartError = Gauge("error_exec_restart_camera", "Camera API - Restart Camera Execution Error", ["customer", "station", "host", "mod", "camera", "url", "endpoint"])
            self.camStatus = Gauge("camera_status", "Camera status - 0 (off) / 1 (on)", ["customer", "station", "host", "camera", "url", "endpoint"])
            self.camHeartbeat = Gauge("camera_heartbeat", "Camera time - heartbeat", ["customer", "station", "host", "camera", "url", "endpoint"])
        # Metric Disk
        if configDict["getDisk"] == 2:
            self.diskSize = Gauge("disk_size", "Disk Size Bytes", ["customer", "station", "host", "volume"])
            self.diskUsed = Gauge("disk_used", "Disk Used Bytes", ["customer", "station", "host", "volume"])
        if configDict["getDisk"] >= 1:
            self.diskExecError = Gauge("error_exec_disk", "Disk - Command Execution Error", ["customer", "station", "host", "mod"])
            self.diskUtilization = Gauge("disk_utilization", "Disk Utilization Percent", ["customer", "station", "host", "volume"])
            self.diskRS = Gauge("disk_read_req_persec", "Disk Read Requests Completed per second", ["customer", "station", "host", "device"])
            self.diskWS = Gauge("disk_write_req_persec", "Disk Write Requests Completed per second", ["customer", "station", "host", "device"])
            self.diskRRQS = Gauge("disk_read_req_queued_persec", "Disk Read Requests per second Queued to the Device", ["customer", "station", "host", "device"])
            self.diskWRQS = Gauge("disk_write_req_queued_persec", "Disk Write Requests per second Queued to the Device", ["customer", "station", "host", "device"])
            self.diskRWait = Gauge("disk_read_await", "Disk Read Average Time (ms)", ["customer", "station", "host", "device"])
            self.diskWWait = Gauge("disk_write_await", "Disk Write Average Time (ms)", ["customer", "station", "host", "device"])
            self.diskAQL = Gauge("disk_avg_queue", "Disk Average Queue Length", ["customer", "station", "host", "device"])
        # Metric Docker
        if configDict["getDocker"] == 2:
            self.dockerPorts = Info("docker_ports", "Docker Image Ports Info", ["customer", "station", "host", "image", "command", "names", "join"])
        if configDict["getDocker"] >= 1:
            self.dockerExecError = Gauge("error_exec_docker", "Docker - Command Execution Error", ["customer", "station", "host", "mod"])
            self.dockerStatusInfo = Info("docker_status_info", "Docker Image Current Status", ["customer", "station", "host", "image", "command", "names", "join"])
            self.dockerStatus = Gauge("docker_status", "Docker Image Current Status", ["customer", "station", "host", "image", "command", "names", "join"])
            self.dockerStatusAge = Gauge("docker_status_age", "Docker Image Current Status Age", ["customer", "station", "host", "image", "command", "names", "join"])
            self.dockerCreated = Gauge("docker_created", "Docker Image Created Age", ["customer", "station", "host", "image", "command", "names", "join"])
        # Metric Nvidia GPU
        if configDict["getGpuNvidia"] == 2:
            self.gpuMulti = Info("gpu_multi", "Multi-GPU Card", ["customer", "station", "host", "card"])
            self.gpuState = Info("gpu_state", "GPU Performance State", ["customer", "station", "host", "card"])
            self.gpuMode = Info("gpu_mode", "GPU Virtualization Mode", ["customer", "station", "host", "card"])
            self.gpuBrand = Info("gpu_brand", "GPU Brand Information", ["customer", "station", "host", "card"])
            self.gpuArch = Info("gpu_arch", "GPU Architecture Information", ["customer", "station", "host", "card"])
            self.gpuDisplayMode = Info("gpu_display_mode", "GPU Display Mode", ["customer", "station", "host", "card"])
            self.gpuDisplayActive = Info("gpu_display_active", "GPU Display Active Info", ["customer", "station", "host", "card"])
        if configDict["getGpuNvidia"] >= 1:
            self.gpuExecError = Gauge("error_exec_gpu", "GPU - Command Execution Error", ["customer", "station", "host", "mod"])
            self.gpuCuda = Info("gpu_cuda", "GPU CUDA Version", ["customer", "station", "host", "card"])
            self.gpuDriver = Info("gpu_driver", "GPU Driver Version", ["customer", "station", "host", "card"])
            self.gpuMemory = Gauge("gpu_memory", "GPU Memory Total", ["customer", "station", "host", "card"])
            self.gpuMemUtilization = Gauge("gpu_mem_utilization", "GPU Memory Utilization Percent", ["customer", "station", "host", "card"])
            self.gpuName = Info("gpu_name", "GPU Name", ["customer", "station", "host", "card"])
            self.gpuPowerDraw = Gauge("gpu_power", "GPU Power Utilization Watts", ["customer", "station", "host", "card"])
            self.gpuTemperature = Gauge("gpu_temperature", "GPU Temperature Celsius", ["customer", "station", "host", "card"])
            self.gpuUtilization = Gauge("gpu_utilization", "GPU Utilization Percent", ["customer", "station", "host", "card"])
            self.gpuFanPct = Gauge("gpu_fan_percent", "GPU Fan Speed Percent", ["customer", "station", "host", "card"])
            self.gpuMemReserved = Gauge("gpu_mem_reserved", "GPU FB Memory Reserved", ["customer", "station", "host", "card"])
            self.gpuMemUsed = Gauge("gpu_mem_used", "GPU FB Memory Used", ["customer", "station", "host", "card"])
            self.gpuMemFree = Gauge("gpu_mem_free", "GPU FB Memory Free", ["customer", "station", "host", "card"])
            self.gpuTempMax = Gauge("gpu_temp_max", "GPU Maximum Temperature", ["customer", "station", "host", "card"])
            self.gpuTempSlow = Gauge("gpu_temp_slow", "GPU Slow Down Temperature", ["customer", "station", "host", "card"])
            self.gpuTempTarget = Gauge("gpu_temp_target", "GPU Operating Target Temperature", ["customer", "station", "host", "card"])
            self.gpuPowerLimit = Gauge("gpu_power_limit", "GPU Power Upper Limit", ["customer", "station", "host", "card"])
            self.gpuPowerMax = Gauge("gpu_power_max", "GPU Maximum Power", ["customer", "station", "host", "card"])
        if configDict["getJetson"] == 2:
            self.jetsonCpuTotal = Gauge("jetson_cpu_total", "Jetson Card Total CPU Count (on+off)", ["customer", "station", "host", "card"])
            self.jetsonPowerThermal = Gauge("jetson_power_thermal", "Jetson Card Power Thermal", ["customer", "station", "host", "card"])
            self.jetsonTempWifi = Gauge("jetson_wifi_temp", "Jetson Card WiFi Temperature", ["customer", "station", "host", "card"])
            self.jetsonNvpModel = Info("jetson_nvp_model", "Jetson Card NVP Model", ["customer", "station", "host", "card"])
        if configDict["getJetson"] >= 1:
            self.jetsonExecError = Gauge("error_exec_jetson", "Jetson Card Command Execution Error", ["customer", "station", "host", "mod"])
            self.jetsonCuda = Info("jetson_cuda", "Jetson Card CUDA Version", ["customer", "station", "host", "card"])
            self.jetsonDriver = Info("jetson_driver", "Jetson Card Driver Version", ["customer", "station", "host", "card"])
            self.jetsonFanPercent = Gauge("jetson_fan_pct", "Jetson Card FAN PWM Percent", ["customer", "station", "host", "card"])
            self.jetsonGpuUse = Gauge("jetson_gpu_utilization", "Jetson Card GPU Utilization", ["customer", "station", "host", "card"])
            self.jetsonCpuAvg = Gauge("jetson_cpu_avg_utilization", "Jetson Card CPU Average Utilization", ["customer", "station", "host", "card"])
            self.jetsonCpuMax = Gauge("jetson_cpu_max_utilization", "Jetson Card CPU Max Utilization", ["customer", "station", "host", "card"])
            self.jetsonMemTotalMB = Gauge("jetson_total_memory", "Jetson Card Memory Total", ["customer", "station", "host", "card"])
            #self.jetsonPower = Gauge("jetson_power", "Jetson Card Power utilization mW", ["customer", "station", "host", "card"])
            self.jetsonMemUsed = Gauge("jetson_memory_utilization", "Jetson Card Memory Utilization", ["customer", "station", "host", "card"])
            self.jetsonTempBoard = Gauge("jetson_temp_board", "Jetson Card Board Temperature", ["customer", "station", "host", "card"])
            self.jetsonTempCpu = Gauge("jetson_temp_cpu", "Jetson Card CPU Temperature", ["customer", "station", "host", "card"])
            self.jetsonTempGpu = Gauge("jetson_temp_gpu", "Jetson Card GPU Temperature", ["customer", "station", "host", "card"])
            #self.jetsonTime = Gauge("jetson_time", "Jetson Card Time Clock", ["customer", "station", "host", "card"])
            #self.jetsonUptime = Gauge("jetson_uptime", "Jetson Card Uptime Seconds", ["customer", "station", "host", "card"])
            self.jetsonName = Info("jetson_name", "Jetson Card GPU Name", ["customer", "station", "host", "card"])
        # Metric Ping
        if configDict["getIpPing"] >= 1:
            self.pingExecError = Gauge("error_exec_ping", "Ping Command Executions Error", ["customer", "station", "host", "mod"])
            self.pingtime = Gauge("ping_exec_time", "Ping time execution", ["customer", "station", "host", "ipaddr"])
            self.pingLoss = Gauge("ping_loss_pct", "Ping loss percentage", ["customer", "station", "host", "ipaddr"])
        # Metric Monitored OS Processes
        if configDict["getMonOsProc"] >= 1:
            self.processCPU = Gauge("process_cpu", "Running Process CPU Usage", ["customer", "station", "host", "process", "proccmd", "join"])
            self.processMEM = Gauge("process_mem", "Running Process Memory Usage", ["customer", "station", "host", "process", "proccmd", "join"])
            self.processPID = Gauge("process_pid", "Running Process PID", ["customer", "station", "host", "process", "proccmd", "join"])
            self.processTime = Gauge("process_time", "Running Process CPU time used (1/100s)", ["customer", "station", "host", "process", "proccmd", "join"])
            self.processActive = Gauge("process_active", "Selected Processes Running Status", ["customer", "station", "host", "process", "proccmd", "join"])
            self.processMissing = Gauge("process_missing", "Selected Processes Running Status", ["customer", "station", "host", "process", "join"])
        # Metric Network
        if configDict["getNetwork"] >= 1:
            self.networkIP = Info("nic_ip", "NIC Card IP Address", ["customer", "station", "host", "nic"])
            self.networkRx = Gauge("nic_rx", "NIC Card UP receiving bytes per second", ["customer", "station", "host", "nic"])
            self.networkTx = Gauge("nic_tx", "NIC Card UP transmiting bytes per second", ["customer", "station", "host", "nic"])
            self.netExecError = Gauge("error_exec_net", "Network Command Execution Error", ["customer", "station", "host", "mod"])
        # Metric Remote Open Port
        if configDict["getRemoteOpen"] >= 1:
            self.remoteOpenExecError = Gauge("error_exec_remote_open", "Remote port open Command Execution Error", ["customer", "station", "host", "mod"])
            self.remoteOpenStatus = Gauge("remote_open_status", "Remote port open status", ["customer", "station", "host", "remoteurl", "join"])
            self.remoteOpenResponse = Info("remote_open_response", "Remote port open response", ["customer", "station", "host", "remoteurl", "join"])
        # Metric Self IP
        if configDict["getSelfIp"] >= 1:
            self.selfIpPresent = Gauge("selfip_present", "Ping time execution", ["customer", "station", "host", "ipaddr"])
        # Metric Server Sensors
        if configDict["getSensor"] == 2:
            self.serverCoreV = Gauge("station_core_voltage", "Station CPU Core Voltage", ["customer", "station", "host", "maxval"])
            self.server3v = Gauge("station_3v_voltage", "Station CPU 3.3v Voltage", ["customer", "station", "host", "maxval"])
            self.server5v = Gauge("station_5v_voltage", "Station CPU 5v Voltage", ["customer", "station", "host", "maxval"])
            self.server12v = Gauge("station_12v_voltage", "Station CPU 12v Voltage", ["customer", "station", "host", "maxval"])
        if configDict["getSensor"] >= 1:
            self.serverSensorExecError = Gauge("error_exec_station_sensor", "Station Sensor Command Execution Error", ["customer", "station", "host", "mod"])
            self.serverChassisFan = Gauge("station_chassis_fan", "Station Chassis Fan RPM", ["customer", "station", "host", "maxval"])
            self.serverCpuFan = Gauge("station_cpu_fan", "Station CPU Fan RPM", ["customer", "station", "host", "maxval"])
            self.serverPciPower = Gauge("station_pci_power", "Station PCI Power", ["customer", "station", "host", "maxval"])
            self.serverCpuTemp = Gauge("station_cpu_temp", "Station CPU Temperature", ["customer", "station", "host", "maxval"])
            self.serverMbTemp = Gauge("station_mb_temp", "Station Motherboard Temperature", ["customer", "station", "host", "maxval"])
            self.serverPciTemp = Gauge("station_pci_temp", "Station PCI Temperature", ["customer", "station", "host", "maxval"])
        # Metric Server Data
        if configDict["getServer"] == 2:
            self.loadAvg1m = Gauge("station_load1m", "Station CPU Load Average 1 minute", ["customer", "station", "host"])
            self.loadAvg5m = Gauge("station_load5m", "Station CPU Load Average 5 minutes", ["customer", "station", "host"])
            self.loadAvg15m = Gauge("station_load15m", "Station CPU Load Average 15 minutes", ["customer", "station", "host"])
            self.utilizationUser = Gauge("station_use_user", "Station CPU User Utilization", ["customer", "station", "host"])
            self.utilizationSystem = Gauge("station_use_system", "Station CPU System Utilization", ["customer", "station", "host"])
            self.taskTotal = Gauge("station_tasks_total", "Station CPU Tasks Total", ["customer", "station", "host"])
            self.taskSleeping = Gauge("station_tasks_sleep", "Station CPU Tasks Sleeping", ["customer", "station", "host"])
            self.taskZombie = Gauge("station_tasks_zombie", "Station CPU Tasks Zombie", ["customer", "station", "host"])
        if configDict["getServer"] >= 1:
            self.serverExecError = Gauge("error_exec_station_server", "Station Server Command Execution Error", ["customer", "station", "host", "mod"])
            self.serverCores = Gauge("station_cores", "Station CPU Cores", ["customer", "station", "host"])
            self.serverMemFree = Gauge("station_mem_free", "Station Memory Free", ["customer", "station", "host"])
            self.serverMemCached = Gauge("station_mem_cached", "Station Memory Cached", ["customer", "station", "host"])
            self.serverMemTotal = Gauge("station_mem_total", "Station Memory Total", ["customer", "station", "host"])
            self.serverMemUsed = Gauge("station_mem_used", "Station Memory Used", ["customer", "station", "host"])
            self.serverUptime = Info("station_uptime", "Station Uptime", ["customer", "station", "host"])
            self.serverTimeStamp = Gauge("station_timestamp", "Station Timestamp", ["customer", "station", "host"])
            self.serverTimeStampUtc = Gauge("station_timestamp_utc", "Station Timestamp UTC", ["customer", "station", "host"])
            self.taskRunning = Gauge("station_tasks_running", "Station CPU Tasks Running", ["customer", "station", "host"])
            self.taskStopped = Gauge("station_tasks_stop", "Station CPU Tasks Stopped", ["customer", "station", "host"])
            self.utilizationIdle = Gauge("station_use_idle", "Station CPU Idle", ["customer", "station", "host"])
        # Metric Sys Agent
        if configDict["getSysAgent"] == 2:
            self.sysagentPID = Gauge("sysagent_pid", "Sys Agent PID", ["customer", "station", "host"])
            self.sysagentMem = Gauge("sysagent_memory", "Sys Agent memory allocated in MB", ["customer", "station", "host"])
        if configDict["getSysAgent"] >= 1:
            self.sysagentExecError = Gauge("error_exec_sysagent", "Sys Agent Command Execution Error", ["customer", "station", "host", "mod"])
            self.sysagentLoaded = Gauge("sysagent_loaded", "Sys Agent is loaded as a service", ["customer", "station", "host"])
            self.sysagentActive = Gauge("sysagent_active", "Sys Agent is active", ["customer", "station", "host"])
            self.sysagentError = Gauge("sysagent_error", "Sys Agent has errors", ["customer", "station", "host"])
        # Metric Top OS Processes
        if configDict["getTopProcess"] >= 1:
            self.topExecError = Gauge("error_exec_top", "Running Top Offender Process Execution Error", ["customer", "station", "host", "mod"])
            self.topProcCPU = Gauge("top_process_cpu", "Running Top Offender Process CPU Usage", ["customer", "station", "host", "rank", "join"])
            self.topProcMEM = Gauge("top_process_mem", "Running Top Offender Process Memory Usage", ["customer", "station", "host", "rank", "join"])
            self.topProcPID = Gauge("top_process_pid", "Running Top Offender Process PID", ["customer", "station", "host", "rank", "join"])
            self.topProcName = Info("top_process_name", "Running Top Offender Process Name", ["customer", "station", "host", "rank", "join"])
        self.configExecError = Gauge("error_exec_config", "Config - Command Execution Error", ["customer", "station", "host", "mod"])
        self.hostArch = Info("station_architecture", "Station CPU Architecture", ["customer", "station", "host"])
        self.hostOsBit = Gauge("station_os_bit_lenght", "Station OS bit lenght", ["customer", "station", "host"])
        self.hostVendorID = Info("station_vendor_id", "Station's Vendor ID", ["customer", "station", "host"])
        self.hostModel = Info("station_model_name", "Station's Model Name", ["customer", "station", "host"])
        self.collectorVersion = Info("agent_version", "Collector Agent Version", ["customer", "station", "host"])
        self.heartBeat = Gauge("station_heartbeat", "Station Heartbeat", ["customer", "station", "host"])
        #self.ntpServerList = Info("ntp_serverlist", "List of configured NTP Servers", ["customer", "station", "host"])
        self.ntpIp = Info("ntp_ip", "In Sync with this NTP Server IP", ["customer", "station", "host"])
        self.ntpDiscrepancy = Gauge("ntp_discrepancy", "Station and NTP server time discrepancy", ["customer", "station", "host"])
        self.ntpPollingPeriod = Gauge("ntp_polling_period", "NTP server polling period", ["customer", "station", "host"])
        self.ntpStatus = Gauge("ntp_status", "NTP status", ["customer", "station", "host"])
        return
        #----------------------------------------------------------------------------------------------------------------------
    def set_data(self):
        # Metric API Get
        if self.configDict["getApiGet"] >= 1:
            self.apiGetExecError.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], mod="apiget").set(self.metricDict["apiGetMetrics"]["apiGetExecError"])
            for element in range(len(self.metricDict["apiGetMetrics"]) - 1):
                if self.configDict["getApiGet"] == 2:
                    self.apiGetUrl.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).info({"api_get_url": self.metricDict["apiGetMetrics"][element]["apiGetUrl"]})
                self.apiGetExists.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], url=self.metricDict["apiGetMetrics"][element]["apiGetUrl"]).set(self.metricDict["apiGetMetrics"][element]["apiGetExists"])
                self.apiGetStatus.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], url=self.metricDict["apiGetMetrics"][element]["apiGetUrl"]).set(self.metricDict["apiGetMetrics"][element]["apiGetStatus"])
                self.apiGetResponse.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], url=self.metricDict["apiGetMetrics"][element]["apiGetUrl"]).info({"api_get_response": self.metricDict["apiGetMetrics"][element]["apiGetResponse"]})
        # Metric Backup
        if self.configDict["getBackup"] >= 1:
            self.bkpExecError.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], mod="backup").set(self.metricDict["bkpMetrics"]["backupExecError"])
            for element in range(len(self.metricDict["bkpMetrics"]) - 1):
                self.bkpStatus.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], path=self.metricDict["bkpMetrics"][element]["path"], name=self.metricDict["bkpMetrics"][element]["name"], join=self.configDict["stationName"]+self.configDict["hostName"]+self.metricDict["bkpMetrics"][element]["name"]).set(self.metricDict["bkpMetrics"][element]["status"])
                self.bkpAccess.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], path=self.metricDict["bkpMetrics"][element]["path"], name=self.metricDict["bkpMetrics"][element]["name"], join=self.configDict["stationName"]+self.configDict["hostName"]+self.metricDict["bkpMetrics"][element]["name"]).set(self.metricDict["bkpMetrics"][element]["access"])
                self.bkpModified.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], path=self.metricDict["bkpMetrics"][element]["path"], name=self.metricDict["bkpMetrics"][element]["name"], join=self.configDict["stationName"]+self.configDict["hostName"]+self.metricDict["bkpMetrics"][element]["name"]).set(self.metricDict["bkpMetrics"][element]["modified"])
                self.bkpExpire.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], path=self.metricDict["bkpMetrics"][element]["path"], name=self.metricDict["bkpMetrics"][element]["name"], join=self.configDict["stationName"]+self.configDict["hostName"]+self.metricDict["bkpMetrics"][element]["name"]).set(self.metricDict["bkpMetrics"][element]["expire_in"])
        # Metric Cam
        if self.configDict["getCam"] >= 1:
            self.camExecError.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], mod="camera").set(self.metricDict["camMetrics"]["camExecError"])
            if self.configDict["camRestart"]:
                try: self.camRestartError.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], mod="camrestart", camera=self.metricDict["camMetrics"][element]["camName"], url=self.metricDict["camMetrics"][element]["camUrl"], endpoint=self.metricDict["camMetrics"][element]["endPoint"]).set(self.metricDict["camMetrics"]["camRestartError"])
                except: self.camRestartError.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], mod="camrestart", camera=self.metricDict["camMetrics"][element]["camName"], url=self.metricDict["camMetrics"][element]["camUrl"], endpoint=self.metricDict["camMetrics"][element]["endPoint"]).set(-1)
            for element in range(len(self.metricDict["camMetrics"]) - 1):
                for subitem in range(len(self.metricDict["camMetrics"][element]) - 1):
                    if self.configDict["getCam"] == 2:
                        self.camSeq.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], camera=self.metricDict["camMetrics"][element][subitem]["camName"], url=self.metricDict["camMetrics"][element]["camUrl"], endpoint=self.metricDict["camMetrics"][element][subitem]["endPoint"]).set(self.metricDict["camMetrics"][element][subitem]["frameSeq"])
                        self.camHeight.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], camera=self.metricDict["camMetrics"][element][subitem]["camName"], url=self.metricDict["camMetrics"][element]["camUrl"], endpoint=self.metricDict["camMetrics"][element][subitem]["endPoint"]).set(self.metricDict["camMetrics"][element][subitem]["camHeight"])
                        self.camWidth.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], camera=self.metricDict["camMetrics"][element][subitem]["camName"], url=self.metricDict["camMetrics"][element]["camUrl"], endpoint=self.metricDict["camMetrics"][element][subitem]["endPoint"]).set(self.metricDict["camMetrics"][element][subitem]["camWidth"])
                    self.camStatus.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], camera=self.metricDict["camMetrics"][element][subitem]["camName"], url=self.metricDict["camMetrics"][element]["camUrl"], endpoint=self.metricDict["camMetrics"][element][subitem]["endPoint"]).set(self.metricDict["camMetrics"][element][subitem]["status"])
                    self.camHeartbeat.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], camera=self.metricDict["camMetrics"][element][subitem]["camName"], url=self.metricDict["camMetrics"][element]["camUrl"], endpoint=self.metricDict["camMetrics"][element][subitem]["endPoint"]).set(self.metricDict["camMetrics"][element][subitem]["camHB"])
        # Metric Disk
        if self.configDict["getDisk"] >= 1:
            if self.metricDict["diskMetrics"]["diskDfExecError"] or self.metricDict["diskMetrics"]["diskExecError"]: self.diskExecError.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], mod="disk").set(1)
            else: self.diskExecError.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], mod="disk").set(0)
            for element in range(len(self.metricDict["diskMetrics"]) - 2):
                if "volume" in self.metricDict["diskMetrics"][element].keys():
                    if self.configDict["getDisk"] == 2:
                        self.diskSize.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], volume=self.metricDict["diskMetrics"][element]["volume"]).set(self.metricDict["diskMetrics"][element]["size"])
                        self.diskUsed.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], volume=self.metricDict["diskMetrics"][element]["volume"]).set(self.metricDict["diskMetrics"][element]["used"])
                    self.diskUtilization.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], volume=self.metricDict["diskMetrics"][element]["volume"]).set(self.metricDict["diskMetrics"][element]["usedPct"])
                elif "device" in self.metricDict["diskMetrics"][element].keys():
                    self.diskRS.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], device=self.metricDict["diskMetrics"][element]["device"]).set(self.metricDict["diskMetrics"][element]["rrps"])
                    self.diskWS.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], device=self.metricDict["diskMetrics"][element]["device"]).set(self.metricDict["diskMetrics"][element]["wrps"])
                    self.diskRRQS.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], device=self.metricDict["diskMetrics"][element]["device"]).set(self.metricDict["diskMetrics"][element]["rrqps"])
                    self.diskWRQS.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], device=self.metricDict["diskMetrics"][element]["device"]).set(self.metricDict["diskMetrics"][element]["wrqps"])
                    self.diskRWait.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], device=self.metricDict["diskMetrics"][element]["device"]).set(self.metricDict["diskMetrics"][element]["rawait"])
                    self.diskWWait.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], device=self.metricDict["diskMetrics"][element]["device"]).set(self.metricDict["diskMetrics"][element]["wawait"])
                    self.diskAQL.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], device=self.metricDict["diskMetrics"][element]["device"]).set(self.metricDict["diskMetrics"][element]["aql"])
        # Metric Docker
        if (self.configDict["getDocker"] >= 1) and (self.metricDict["dockerMetrics"] != 0):
            self.dockerExecError.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], mod="docker").set(self.metricDict["dockerMetrics"]["dockerExecError"])
            for element in range(len(self.metricDict["dockerMetrics"]) - 1):
                imageInfo = self.metricDict["dockerMetrics"][element]["image"]
                portsInfo = self.metricDict["dockerMetrics"][element]["ports"]
                statusInfo = self.metricDict["dockerMetrics"][element]["status"]
                if statusInfo == "up": statusGauge = 1
                else: statusGauge = 0
                if self.configDict["getDocker"] == 2:
                    self.dockerPorts.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], image=imageInfo, command=self.metricDict["dockerMetrics"][element]["command"], names=self.metricDict["dockerMetrics"][element]["names"], join=self.configDict["stationName"]+self.configDict["hostName"]+self.metricDict["dockerMetrics"][element]["names"]).info({"docker_ports": portsInfo})
                self.dockerStatusInfo.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], image=imageInfo, command=self.metricDict["dockerMetrics"][element]["command"], names=self.metricDict["dockerMetrics"][element]["names"], join=self.configDict["stationName"]+self.configDict["hostName"]+self.metricDict["dockerMetrics"][element]["names"]).info({"docker_status_info": statusInfo})
                self.dockerStatus.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], image=imageInfo, command=self.metricDict["dockerMetrics"][element]["command"], names=self.metricDict["dockerMetrics"][element]["names"], join=self.configDict["stationName"]+self.configDict["hostName"]+self.metricDict["dockerMetrics"][element]["names"]).set(statusGauge)
                self.dockerStatusAge.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], image=imageInfo, command=self.metricDict["dockerMetrics"][element]["command"], names=self.metricDict["dockerMetrics"][element]["names"], join=self.configDict["stationName"]+self.configDict["hostName"]+self.metricDict["dockerMetrics"][element]["names"]).set(self.metricDict["dockerMetrics"][element]["statusTime"])
                self.dockerCreated.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], image=imageInfo, command=self.metricDict["dockerMetrics"][element]["command"], names=self.metricDict["dockerMetrics"][element]["names"], join=self.configDict["stationName"]+self.configDict["hostName"]+self.metricDict["dockerMetrics"][element]["names"]).set(self.metricDict["dockerMetrics"][element]["created"])
        # Metric Nvidia GPU
        if self.configDict["getGpuNvidia"] >= 1:
            self.gpuExecError.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], mod="gpu_x86").set(self.metricDict["gpuMetrics"]["gpuExecError"])
            if self.configDict["getGpuNvidia"] == 2:
                self.gpuMulti.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).info({"gpu_multi": self.metricDict["gpuMetrics"]["multiGpu"]})
                self.gpuState.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).info({"gpu_state": self.metricDict["gpuMetrics"]["performanceState"]})
                self.gpuMode.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).info({"gpu_mode": self.metricDict["gpuMetrics"]["virtMode"]})
                self.gpuBrand.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).info({"gpu_brand": self.metricDict["gpuMetrics"]["gpuBrand"]})
                self.gpuArch.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).info({"gpu_arch": self.metricDict["gpuMetrics"]["gpuArch"]})
                self.gpuDisplayMode.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).info({"gpu_display_mode": self.metricDict["gpuMetrics"]["gpuDisplayMode"]})
                self.gpuDisplayActive.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).info({"gpu_display_active": self.metricDict["gpuMetrics"]["gpuDisplayActive"]})
            self.gpuCuda.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).info({"gpu_cuda": self.metricDict["gpuMetrics"]["cuda"]})
            self.gpuDriver.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).info({"gpu_driver": self.metricDict["gpuMetrics"]["driver"]})
            self.gpuMemory.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).set(self.metricDict["gpuMetrics"]["memTotal"])
            self.gpuMemUtilization.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).set(self.metricDict["gpuMetrics"]["memUtil"])
            self.gpuName.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).info({"gpu_name": self.metricDict["gpuMetrics"]["gpuName"]})
            self.gpuPowerDraw.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).set(self.metricDict["gpuMetrics"]["powerDraw"])
            self.gpuTemperature.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).set(self.metricDict["gpuMetrics"]["temperature"])
            self.gpuUtilization.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).set(self.metricDict["gpuMetrics"]["gpuUtil"])
            self.gpuFanPct.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).set(self.metricDict["gpuMetrics"]["fanSpeed"])
            self.gpuMemReserved.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).set(self.metricDict["gpuMetrics"]["memReserved"])
            self.gpuMemUsed.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).set(self.metricDict["gpuMetrics"]["memUsed"])
            self.gpuMemFree.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).set(self.metricDict["gpuMetrics"]["memFree"])
            self.gpuTempMax.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).set(self.metricDict["gpuMetrics"]["tempMax"])
            self.gpuTempSlow.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).set(self.metricDict["gpuMetrics"]["tempSlowDn"])
            self.gpuTempTarget.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).set(self.metricDict["gpuMetrics"]["tempTarget"])
            self.gpuPowerLimit.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).set(self.metricDict["gpuMetrics"]["powerLimit"])
            self.gpuPowerMax.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["gpuMetrics"]["card"]).set(self.metricDict["gpuMetrics"]["powerMax"])
        # Metric Jetson GPU
        if self.configDict["getJetson"] == 2:
            self.jetsonCpuTotal.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["jetsonMetrics"]["card"]).set(self.metricDict["jetsonMetrics"]["cpuTotalCount"])
            self.jetsonPowerThermal.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["jetsonMetrics"]["card"]).set(self.metricDict["jetsonMetrics"]["powerThermal"])
            self.jetsonTempWifi.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["jetsonMetrics"]["card"]).set(self.metricDict["jetsonMetrics"]["tempWifi"])
            self.jetsonNvpModel.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["jetsonMetrics"]["card"]).info({"jetson_nvp_model": self.metricDict["jetsonMetrics"]["nvpModel"]})
        if self.configDict["getJetson"] >= 1:
            if self.metricDict["jetsonMetrics"]["jetsonExecError"]: self.jetsonExecError.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], mod="gpu_arm").set(1)
            else: self.jetsonExecError.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], mod="gpuarm").set(0)
            self.jetsonCuda.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["jetsonMetrics"]["card"]).info({"jetson_cuda": str(self.metricDict["jetsonMetrics"]["cuda"])})
            self.jetsonDriver.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["jetsonMetrics"]["card"]).info({"jetson_driver": str(self.metricDict["jetsonMetrics"]["driver"])})
            self.jetsonFanPercent.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["jetsonMetrics"]["card"]).set(self.metricDict["jetsonMetrics"]["fanPercent"])
            self.jetsonGpuUse.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["jetsonMetrics"]["card"]).set(self.metricDict["jetsonMetrics"]["gpuUse"])
            self.jetsonCpuAvg.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["jetsonMetrics"]["card"]).set(self.metricDict["jetsonMetrics"]["cpuAvgUse"])
            self.jetsonCpuMax.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["jetsonMetrics"]["card"]).set(self.metricDict["jetsonMetrics"]["cpuMaxUse"])
            self.jetsonMemTotalMB.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["jetsonMetrics"]["card"]).set(self.metricDict["jetsonMetrics"]["memTotalMB"])
            #self.jetsonPower.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["jetsonMetrics"]["card"]).set(self.metricDict["jetsonMetrics"]["powerTotal"])
            self.jetsonMemUsed.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["jetsonMetrics"]["card"]).set(self.metricDict["jetsonMetrics"]["ramUsed"])
            self.jetsonTempBoard.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["jetsonMetrics"]["card"]).set(self.metricDict["jetsonMetrics"]["tempBoard"])
            self.jetsonTempCpu.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["jetsonMetrics"]["card"]).set(self.metricDict["jetsonMetrics"]["tempCPU"])
            self.jetsonTempGpu.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["jetsonMetrics"]["card"]).set(self.metricDict["jetsonMetrics"]["tempGPU"])
            #self.jetsonTime.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["jetsonMetrics"]["card"]).set(self.metricDict["jetsonMetrics"]["time"])
            #self.jetsonUptime.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["jetsonMetrics"]["card"]).set(self.metricDict["jetsonMetrics"]["uptime"])
            self.jetsonName.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], card=self.metricDict["jetsonMetrics"]["card"]).info({"jetson_name": self.metricDict["jetsonMetrics"]["gpuName"]})
        # Metric Ping
        if self.configDict["getIpPing"] >= 1:
            if self.metricDict["pingMetrics"] != 0: self.pingExecError.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], mod="ping").set(self.metricDict["pingMetrics"]["pingExecError"])
            for item in range(len(self.metricDict["pingMetrics"]) - 1):
                self.pingtime.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], ipaddr=self.metricDict["pingMetrics"][item]["ipAddr"].strip()).set(self.metricDict["pingMetrics"][item]["resp"]["execTime"])
                self.pingLoss.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], ipaddr=self.metricDict["pingMetrics"][item]["ipAddr"].strip()).set(self.metricDict["pingMetrics"][item]["resp"]["packLoss"])
        # Metric Monitored OS Processes
        if self.configDict["getMonOsProc"] >= 1:
            if len(self.metricDict["monOsProcMetrics"]) > 3:
                for element in range(len(self.metricDict["monOsProcMetrics"]) - 3):
                    self.processTime.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], process=self.metricDict["monOsProcMetrics"][element]["processCfg"], proccmd=self.metricDict["monOsProcMetrics"][element]["cmd"], join=self.configDict["stationName"]+self.configDict["hostName"]+str(self.metricDict["monOsProcMetrics"][element]["pid"])).set(self.metricDict["monOsProcMetrics"][element]["time"])
                    self.processCPU.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], process=self.metricDict["monOsProcMetrics"][element]["processCfg"], proccmd=self.metricDict["monOsProcMetrics"][element]["cmd"], join=self.configDict["stationName"]+self.configDict["hostName"]+str(self.metricDict["monOsProcMetrics"][element]["pid"])).set(self.metricDict["monOsProcMetrics"][element]["cpu"])
                    self.processMEM.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], process=self.metricDict["monOsProcMetrics"][element]["processCfg"], proccmd=self.metricDict["monOsProcMetrics"][element]["cmd"], join=self.configDict["stationName"]+self.configDict["hostName"]+str(self.metricDict["monOsProcMetrics"][element]["pid"])).set(self.metricDict["monOsProcMetrics"][element]["mem"])
                    self.processPID.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], process=self.metricDict["monOsProcMetrics"][element]["processCfg"], proccmd=self.metricDict["monOsProcMetrics"][element]["cmd"], join=self.configDict["stationName"]+self.configDict["hostName"]+str(self.metricDict["monOsProcMetrics"][element]["pid"])).set(self.metricDict["monOsProcMetrics"][element]["pid"])
                    self.processActive.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], process=self.metricDict["monOsProcMetrics"][element]["processCfg"], proccmd=self.metricDict["monOsProcMetrics"][element]["cmd"], join=self.configDict["stationName"]+self.configDict["hostName"]+str(self.metricDict["monOsProcMetrics"][element]["pid"])).set(self.metricDict["monOsProcMetrics"][element]["processActive"])
                self.processMissing.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], process=self.metricDict["monOsProcMetrics"][element]["processCfg"], join=self.configDict["stationName"]+self.configDict["hostName"]+str(self.metricDict["monOsProcMetrics"][element]["pid"])).set(len(self.metricDict["monOsProcMetrics"]["missingProcess"]))
        # Metric Network
        if self.configDict["getNetwork"] >= 1:
            self.netExecError.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], mod="monit_os_proc").set(self.metricDict["netMetrics"]["netexecerror"])
            for element in range(len(self.metricDict["netMetrics"]) - 1):
                self.networkIP.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], nic=self.metricDict["netMetrics"][element]["name"]).info({"ip": self.metricDict["netMetrics"][element]["ipAddr"]})
                self.networkRx.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], nic=self.metricDict["netMetrics"][element]["name"]).set(self.metricDict["netMetrics"][element]["rxBps"])
                self.networkTx.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], nic=self.metricDict["netMetrics"][element]["name"]).set(self.metricDict["netMetrics"][element]["txBps"])
        # Metric Remote Open Port
        if self.configDict["getRemoteOpen"] >= 1:
            self.remoteOpenExecError.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], mod="remote_open").set(self.metricDict["remoteOpenMetrics"]["remoteOpenExecError"])
            for element in range(len(self.metricDict["remoteOpenMetrics"]) - 1):
                self.remoteOpenStatus.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], remoteurl=self.metricDict["remoteOpenMetrics"][element]["remoteOpenUrl"], join=self.configDict["stationName"]+self.configDict["hostName"]+str(self.metricDict["remoteOpenMetrics"][element]["remoteOpenUrl"])).set(self.metricDict["remoteOpenMetrics"][element]["remoteOpenStatus"])
                self.remoteOpenResponse.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], remoteurl=self.metricDict["remoteOpenMetrics"][element]["remoteOpenUrl"], join=self.configDict["stationName"]+self.configDict["hostName"]+str(self.metricDict["remoteOpenMetrics"][element]["remoteOpenUrl"])).info({"remote_open_response": self.metricDict["remoteOpenMetrics"][element]["remoteOpenResponse"]})
        # Metric Self IP
        if self.configDict["getSelfIp"] >= 1:
            if len(self.metricDict["selfIpMetrics"]) > 0:
                for listItem in range(len(self.metricDict["selfIpMetrics"]) - 1):
                    self.selfIpPresent.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], ipaddr=self.metricDict["selfIpMetrics"][listItem]["ip"]).set(self.metricDict["selfIpMetrics"][listItem]["present"])
        # Metric Server Sensors
        if self.configDict["getSensor"] == 2:
            self.serverCoreV.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], maxval=self.metricDict["sensorMetrics"]["vCoreMax"]).set(self.metricDict["sensorMetrics"]["vCore"])
            self.server3v.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], maxval=self.metricDict["sensorMetrics"]["v3.3Max"]).set(self.metricDict["sensorMetrics"]["v3.3"])
            self.server5v.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], maxval=self.metricDict["sensorMetrics"]["v5.0Max"]).set(self.metricDict["sensorMetrics"]["v5.0"])
            self.server12v.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], maxval=self.metricDict["sensorMetrics"]["v12.0Max"]).set(self.metricDict["sensorMetrics"]["v12.0"])
        if self.configDict["getSensor"] >= 1:
            self.serverSensorExecError.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], mod="sensor").set(self.metricDict["sensorMetrics"]["sensorExecError"])
            self.serverChassisFan.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], maxval=self.metricDict["sensorMetrics"]["chassisFanRpmMax"]).set(self.metricDict["sensorMetrics"]["chassisFanRPM"])
            self.serverCpuFan.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], maxval=self.metricDict["sensorMetrics"]["cpuFanRpmMax"]).set(self.metricDict["sensorMetrics"]["cpuFanRPM"])
            self.serverPciPower.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], maxval=self.metricDict["sensorMetrics"]["pciPowerMax"]).set(self.metricDict["sensorMetrics"]["pciPower"])
            self.serverCpuTemp.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], maxval=self.metricDict["sensorMetrics"]["cpuTempMax"]).set(self.metricDict["sensorMetrics"]["cpuTemp"])
            self.serverMbTemp.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], maxval=self.metricDict["sensorMetrics"]["mbTempMax"]).set(self.metricDict["sensorMetrics"]["mbTemp"])
            self.serverPciTemp.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], maxval=self.metricDict["sensorMetrics"]["pciTempMax"]).set(self.metricDict["sensorMetrics"]["pciTemp"])
        # Metric Server Data
        if self.configDict["getServer"] == 2:
            self.loadAvg1m.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).set(self.metricDict["serverMetrics"]["loadAvg1m"])
            self.loadAvg5m.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).set(self.metricDict["serverMetrics"]["loadAvg5m"])
            self.loadAvg15m.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).set(self.metricDict["serverMetrics"]["loadAvg15m"])
            self.utilizationUser.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).set(self.metricDict["serverMetrics"]["cpuUser"])
            self.utilizationSystem.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).set(self.metricDict["serverMetrics"]["cpuSys"])
            self.taskTotal.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).set(self.metricDict["serverMetrics"]["taskTotal"])
            self.taskSleeping.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).set(self.metricDict["serverMetrics"]["taskSleeping"])
            self.taskZombie.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).set(self.metricDict["serverMetrics"]["taskZombie"])
        if self.configDict["getServer"] >= 1:
            self.serverExecError.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], mod="server").set(self.metricDict["serverMetrics"]["serverExecError"])
            self.serverCores.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).set(self.metricDict["serverMetrics"]["cpuCores"])
            self.serverMemFree.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).set(self.metricDict["serverMetrics"]["memFree"])
            self.serverMemCached.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).set(self.metricDict["serverMetrics"]["memCached"])
            self.serverMemTotal.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).set(self.metricDict["serverMetrics"]["memTotal"])
            self.serverMemUsed.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).set(self.metricDict["serverMetrics"]["memUsed"])
            self.serverUptime.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).info({"station_uptime": self.metricDict["serverMetrics"]["serverUp"]})
            self.serverTimeStamp.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).set(self.metricDict["serverMetrics"]["servertime"])
            self.serverTimeStampUtc.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).set(self.metricDict["serverMetrics"]["servertimeUTC"])
            self.taskRunning.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).set(self.metricDict["serverMetrics"]["taskRunning"])
            self.taskStopped.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).set(self.metricDict["serverMetrics"]["taskStopped"])
            self.utilizationIdle.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).set(self.metricDict["serverMetrics"]["cpuIdle"])
        # Metric Sys Agent
        if self.configDict["getSysAgent"] == 2:
            self.sysagentPID.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).set(self.metricDict["sysAgentMetrics"]["saPID"])
            self.sysagentMem.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).set(self.metricDict["sysAgentMetrics"]["saMEM"])
        if self.configDict["getSysAgent"] >= 1:
            if self.metricDict["sysAgentMetrics"]["sysagentExecError"] or self.metricDict["sysAgentMetrics"]["restartExecError"]: self.sysagentExecError.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], mod="sysagent").set(1)
            else: self.sysagentExecError.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], mod="sysagent").set(0)
            if self.metricDict["sysAgentMetrics"]["saLoaded"] == "loaded": saL = 1
            else: saL = 0
            if self.metricDict["sysAgentMetrics"]["saActive"] == "active": saA = 1
            else: saA = 0
            self.sysagentLoaded.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).set(saL)
            self.sysagentActive.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).set(saA)
            self.sysagentError.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).set(self.metricDict["sysAgentMetrics"]["saError"])
        # Metric Top OS Processes
        if self.configDict["getTopProcess"] >= 1:
            self.topExecError.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], mod="top_proc").set(self.metricDict["topMetrics"]["topExecError"])
            for element in range(len(self.metricDict["topMetrics"]) - 1):
                self.topProcCPU.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], rank=self.metricDict["topMetrics"][element]["rank"], join=str(self.metricDict["topMetrics"][element]["rank"])+"-"+self.configDict["hostName"]).set(self.metricDict["topMetrics"][element]["cpu"])
                self.topProcMEM.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], rank=self.metricDict["topMetrics"][element]["rank"], join=str(self.metricDict["topMetrics"][element]["rank"])+"-"+self.configDict["hostName"]).set(self.metricDict["topMetrics"][element]["mem"])
                self.topProcPID.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], rank=self.metricDict["topMetrics"][element]["rank"], join=str(self.metricDict["topMetrics"][element]["rank"])+"-"+self.configDict["hostName"]).set(self.metricDict["topMetrics"][element]["pid"])
                self.topProcName.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], rank=self.metricDict["topMetrics"][element]["rank"], join=str(self.metricDict["topMetrics"][element]["rank"])+"-"+self.configDict["hostName"]).info({"top_process_name": self.metricDict["topMetrics"][element]["cmd"]})
        self.configExecError.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"], mod="config").set(self.configDict["configExecError"])
        self.hostArch.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).info({"station_architecture": self.configDict["cpuArch"]})
        self.hostOsBit.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).set(self.configDict["cpuBit"])
        self.hostVendorID.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).info({"station_vendor_id": self.configDict["cpuVendor"]})
        self.hostModel.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).info({"station_model_name": self.configDict["cpuModelName"]})
        self.collectorVersion.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).info({"agent_version": versao})
        self.heartBeat.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).set(time.time())
        #self.ntpServerList.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).info({"ntp_ip": self.configDict["ntpServerList"]})
        self.ntpIp.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).info({"ntp_ip": self.configDict["ntpIp"]})
        self.ntpDiscrepancy.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).set(self.configDict["ntpTimeDiscrepancy"])
        self.ntpPollingPeriod.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).set(self.configDict["ntpPollingPeriod"])
        self.ntpStatus.labels(customer=self.configDict["customerName"], station=self.configDict["stationName"], host=self.configDict["hostName"]).set(self.configDict["ntpStatus"])
        return
        #----------------------------------------------------------------------------------------------------------------------