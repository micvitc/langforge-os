import psutil
import subprocess
from langchain_core.tools import tool


@tool
def check_sys_tool():
    """Get the system information."""

    cpu_info = {
        "Physical Cores": psutil.cpu_count(logical=False),
        "Total Cores": psutil.cpu_count(logical=True),
        "CPU Frequency (MHz)": psutil.cpu_freq().current,
        "CPU Usage (%)": psutil.cpu_percent(interval=1),
    }

    memory_info = psutil.virtual_memory()
    memory_details = {
        "Total Memory (GB)": round(memory_info.total / (1024**3), 2),
        "Available Memory (GB)": round(memory_info.available / (1024**3), 2),
        "Memory Usage (%)": memory_info.percent,
    }

    disk_info = psutil.disk_usage("/mnt/c")
    disk_details = {
        "Total Disk Space (GB)": round(disk_info.total / (1024**3), 2),
        "Used Disk Space (GB)": round(disk_info.used / (1024**3), 2),
        "Free Disk Space (GB)": round(disk_info.free / (1024**3), 2),
        "Disk Usage (%)": disk_info.percent,
    }

    return {
        "CPU Info": cpu_info,
        "Memory Info": memory_details,
        "Disk Info": disk_details,
    }


@tool
def run_process(command: str):
    """Run a command in the shell."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    return result.stdout if result.returncode == 0 else result.stderr


tools = [check_sys_tool, run_process]
