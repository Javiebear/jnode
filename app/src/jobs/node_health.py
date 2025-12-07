# File: node_health.py
# Author: Javier Chung
# Date: 11/13/25
# Description: This program is used to gather data on a node

# Project Modules
from logger import setup_logger
# Python Libraries
from datetime import timedelta
import subprocess

# Logger setup
logger, listener = setup_logger()

def run_cmd(cmd):
    """
        This method will run a shell command and return the entire result
    """
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        logger.info(f"data retrieved: {result}")
        return result.stdout.strip()

    except Exception as e:
        logger.info(f"failed to retrieve data with cmd: '{cmd}' with error: {e}")
        return None

def get_cpu_perc():
    """
        This method will return the cpu usage in a percentage
    """
    cmd = "top -bn1 | grep 'Cpu(s)' | awk '{print 100 - $8}'"


    return float(run_cmd(cmd))

def get_cpu_temp():
    """
        Get temp of cpu
        
        returns:
          cpu temp in celcius
    """
    temp = run_cmd("cat /sys/class/thermal/thermal_zone0/temp")
    return round(int(temp) / 1000.0, 1)

def get_mem():
    """
        Gets memory usage

        returns:
            dict: {total ram, used ram, free ram} 
    """
    mem = run_cmd("free -m | awk 'NR==2{print $2, $3, $4}'").split()
    return {
        "total": int(mem[0]),
        "used": int(mem[1]),
        "free": int(mem[2]),
    }

def get_storage():
    """
        gets total storage used

        returns:
            dict: {total storage, used storage, free storage}
    """

    storage = run_cmd("df -m / | awk 'NR==2 {print $2, $3, $4}'").split()
    return {
        "total": int(storage[0]),
        "used": int(storage[1]),
        "free": int(storage[2]),
    }

def get_data():
    """
        This method will retrieve all data of a linux node

        returns:
            dict: {cpu usage percentage, cpu tempertature, ram usage, storage usage}
    """
    logger.info(f"Retrieving node data...")

    return {
        "cpu_percent": get_cpu_perc(),
        "cpu_temp": get_cpu_temp(),
        "memory_usage": get_mem(),
        "storage_usage": get_storage()
    }