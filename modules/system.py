import platform
import psutil
import os
import sys
import datetime
import socket
import subprocess

# --- SYSTEM OPERATIONS (1-30) ---

def get_sys_info(params):
    return {"status": "success", "info": {"os": platform.system(), "version": platform.release(), "arch": platform.machine()}}

def get_cpu_usage(params):
    return {"status": "success", "usage": psutil.cpu_percent(interval=1)}

def get_ram_usage(params):
    return {"status": "success", "ram": psutil.virtual_memory().percent}

def get_disk_space(params):
    return {"status": "success", "disk": psutil.disk_usage('/').percent}

def get_os_version(params):
    return {"status": "success", "version": platform.platform()}

def list_processes(params):
    return {"status": "success", "procs": [{"pid": p.pid, "name": p.info['name']} for p in psutil.process_iter(['pid', 'name'])]}

def kill_process(params):
    psutil.Process(params.get("pid")).terminate()
    return {"status": "success"}

def get_uptime(params):
    return {"status": "success", "uptime": datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())}

def get_boot_time(params):
    return {"status": "success", "boot": datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")}

def get_user_info(params):
    return {"status": "success", "user": os.getlogin()}

def get_env_vars(params):
    return {"status": "success", "vars": dict(os.environ)}

def get_battery(params):
    battery = psutil.sensors_battery()
    return {"status": "success", "percent": battery.percent if battery else "N/A"}

def get_gpu_info(params):
    # Simplified hardware lookup
    return {"status": "success", "gpu": "Not detected (Use specialized lib)"}

def get_installed_apps(params):
    # Simplified list
    return {"status": "success", "apps": os.listdir("C:\\Program Files") if os.name == 'nt' else []}

def get_cpu_temp(params):
    # Requires hardware support
    return {"status": "success", "temp": "Check BIOS"}

def get_lang(params):
    return {"status": "success", "lang": platform.win32_ver() if os.name == 'nt' else "Linux"}

def get_kbd_layout(params):
    return {"status": "success", "layout": "US"}

def list_services(params):
    return {"status": "success", "services": [s.name() for s in psutil.win_service_iter()] if os.name == 'nt' else []}

def get_timezone(params):
    return {"status": "success", "tz": datetime.datetime.now().astimezone().tzname()}

def check_admin(params):
    import ctypes
    return {"status": "success", "admin": ctypes.windll.shell32.IsUserAnAdmin() != 0 if os.name == 'nt' else False}

def set_env_var(params):
    os.environ[params.get("key")] = params.get("value")
    return {"status": "success"}

def get_proc_name(params):
    p = psutil.Process(params.get("pid"))
    return {"status": "success", "name": p.name()}

def suspend_proc(params):
    psutil.Process(params.get("pid")).suspend()
    return {"status": "success"}

def resume_proc(params):
    psutil.Process(params.get("pid")).resume()
    return {"status": "success"}

def get_current_pid(params):
    return {"status": "success", "pid": os.getpid()}

def get_all_users(params):
    return {"status": "success", "users": [u.name for u in psutil.users()]}

def get_uuid(params):
    return {"status": "success", "uuid": subprocess.getoutput("wmic csproduct get uuid") if os.name == 'nt' else "N/A"}

def is_vm(params):
    return {"status": "success", "vm": False}

def get_machine_model(params):
    return {"status": "success", "model": subprocess.getoutput("wmic csproduct get name") if os.name == 'nt' else "Physical"}

def get_bios(params):
    return {"status": "success", "bios": subprocess.getoutput("wmic bios get smbiosbiosversion") if os.name == 'nt' else "N/A"}

# --- ROUTER MAP ---
functions = {
    "sys_info": get_sys_info, "cpu_usage": get_cpu_usage, "ram_usage": get_ram_usage,
    "disk_space": get_disk_space, "os_ver": get_os_version, "list_procs": list_processes,
    "kill_proc": kill_process, "uptime": get_uptime, "boot_time": get_boot_time,
    "user_info": get_user_info, "env_vars": get_env_vars, "battery": get_battery,
    "gpu_info": get_gpu_info, "apps": get_installed_apps, "cpu_temp": get_cpu_temp,
    "lang": get_lang, "kbd_layout": get_kbd_layout, "services": list_services,
    "timezone": get_timezone, "is_admin": check_admin, "set_env": set_env_var,
    "proc_name": get_proc_name, "suspend_proc": suspend_proc, "resume_proc": resume_proc,
    "pid": get_current_pid, "users": get_all_users, "uuid": get_uuid,
    "is_vm": is_vm, "model": get_machine_model, "bios": get_bios
}
