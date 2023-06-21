#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#######################################################################################################################
versao = "metricsysagent-v5.00-beta-test"
#######################################################################################################################
import logging
import time
from lib import common as c
#######################################################################################################################
c.versionDict["metricsysagent"] = versao
#######################################################################################################################
class sys_agent_exec:
    # Execute Sys Agent metric collector
    def collect_sys_agent(getSysAgent, sysAgentRestart):
        sysagentout = ""
        if getSysAgent:
            if not c.logFirstRun: logging.info(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-metricsysagent version: {versao}")
            sysagentout = ""
            try: sysagentout = c.exec_cmd(["systemctl", "status", "sys_agent.service"], c.debugMode)["output"].splitlines()
            except: 
                if not c.logFirstRun: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-sys_agent_exec.collect_sys_agent: SysAgent execution error")
        if sysagentout != "": sysAgentMetrics = sys_agent_exec.sys_agent_metrics(sysagentout, sysAgentRestart)
        else: sysAgentMetrics = 0
        return sysAgentMetrics
        #----------------------------------------------------------------------------------------------------------------------
    def sys_agent_metrics(sysagentout, sysAgentRestart):
        resposta = {
            "saLoaded": 0,
            "saActive": 0,
            "saPID": 0,
            "saMEM": 0,
            "saError": 0}
        for element in range(len(sysagentout)):
            if "Loaded" in sysagentout[element]:
                resposta["saLoaded"] = sysagentout[element].split("Loaded")[1][1:].strip().split()[0]
            if "Active" in sysagentout[element]:
                resposta["saActive"] = sysagentout[element].split("Active")[1][1:].strip().split()[0]
            if "PID" in sysagentout[element]:
                resposta["saPID"] = int(sysagentout[element].split(":")[1].split("(")[0].strip())
            if "Memory" in sysagentout[element]:
                saMem = sysagentout[element].split("Memory")[1]
                if saMem[-1] == "K": multi = 1024
                elif saMem[-1] == "M": multi = 1024 * 1024
                elif saMem[-1] == "G": multi = 1024 * 1024 * 1024
                if isinstance(saMem[1:].replace(",", "."), (int, float)): 
                    resposta["saMEM"] = float(saMem[1:].replace(",", ".")) * multi
                else: 
                    resposta["saMEM"] = float(saMem[1:-1].replace(",", ".")) * multi
            if "ERROR" in sysagentout[element]: 
                resposta["saError"] = 1
                sys_agent_exec.sysagent_restart(sysagentout, sysAgentRestart)
        return resposta
        #----------------------------------------------------------------------------------------------------------------------
    def sysagent_restart(sysagentout, sysAgentRestart):
        if sysAgentRestart:
            import subprocess
            errorcount = 0
            for element in range(len(sysagentout)):
                if "ERROR" in sysagentout[element]:
                    logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-sys_agent_exec.sysagent_restart: {sysagentout[element]}")
                    errorcount += 1
            if errorcount > 0: c.sysAgentCount += 1
            if c.sysAgentCount > 3:
                try: reSA = subprocess.call('echo $SAMON | sudo -S systemctl restart sys_agent.service', shell = True)
                except: logging.error(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()))}-sys_agent_exec.sysagent_restart: Error restarting sysagent")
                c.sysAgentCount = 0
        return
        #----------------------------------------------------------------------------------------------------------------------
