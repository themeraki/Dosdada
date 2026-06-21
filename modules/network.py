import socket
import subprocess
import requests
import platform
import os

# --- NETWORK OPERATIONS (31-60) ---

def get_public_ip(params):
    try:
        ip = requests.get('https://api.ipify.org').text
        return {"status": "success", "ip": ip}
    except:
        return {"status": "error", "message": "Failed to reach IP service"}

def list_interfaces(params):
    import psutil
    return {"status": "success", "interfaces": list(psutil.net_if_addrs().keys())}

def ping_host(params):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    res = subprocess.run(['ping', param, '1', params.get('host')], capture_output=True)
    return {"status": "success", "output": res.returncode == 0}

def scan_port(params):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        res = s.connect_ex((params.get('host'), int(params.get('port'))))
        s.close()
        return {"status": "success", "open": res == 0}
    except:
        return {"status": "error"}

def get_dns_settings(params):
    return {"status": "success", "output": subprocess.getoutput("ipconfig /displaydns" if platform.system() == "Windows" else "cat /etc/resolv.conf")}

def flush_dns(params):
    cmd = "ipconfig /flushdns" if platform.system() == "Windows" else "sudo killall -HUP mDNSResponder"
    return {"status": "success", "output": subprocess.getoutput(cmd)}

def get_arp_table(params):
    return {"status": "success", "table": subprocess.getoutput("arp -a")}

def netstat_view(params):
    return {"status": "success", "connections": subprocess.getoutput("netstat -ano")}

def download_url(params):
    try:
        r = requests.get(params.get("url"), stream=True)
        with open(params.get("dest"), 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): f.write(chunk)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def check_internet(params):
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return {"status": "success", "connected": True}
    except:
        return {"status": "success", "connected": False}

# --- STUBS & UTILITIES (41-60) ---
def get_hostname(p): return {"status": "success", "hostname": socket.gethostname()}
def get_fqdn(p): return {"status": "success", "fqdn": socket.getfqdn()}
def traceroute(p): return {"status": "success", "trace": subprocess.getoutput(f"tracert {p.get('host')}" if platform.system()=="Windows" else f"traceroute {p.get('host')}")}
def get_gateway(p): return {"status": "success", "gw": "192.168.1.1"} # Simplified
def resolve_dns(p): return {"status": "success", "ip": socket.gethostbyname(p.get('host'))}
def list_wifi(p): return {"status": "success", "networks": subprocess.getoutput("netsh wlan show networks") if platform.system() == "Windows" else "N/A"}
def disconnect_wifi(p): os.system("netsh wlan disconnect"); return {"status": "success"}
def get_routing_table(p): return {"status": "success", "routes": subprocess.getoutput("route print" if platform.system()=="Windows" else "netstat -rn")}
def tcp_send(p): return {"status": "success", "sent": True}
def udp_send(p): return {"status": "success", "sent": True}
def enable_firewall(p): os.system("netsh advfirewall set allprofiles state on"); return {"status": "success"}
def disable_firewall(p): os.system("netsh advfirewall set allprofiles state off"); return {"status": "success"}
def get_mac_address(p): return {"status": "success", "mac": "00:00:00:00:00:00"}
def tunnel_test(p): return {"status": "success", "tunnel": "active"}
def set_proxy(p): return {"status": "success", "proxy": "set"}
def unset_proxy(p): return {"status": "success", "proxy": "unset"}
def port_listen(p): return {"status": "success", "listening": True}
def get_connection_speed(p): return {"status": "success", "speed": "100Mbps"}
def ping_gateway(p): return {"status": "success", "ping": True}
def detect_vpn(p): return {"status": "success", "vpn": False}

# --- ROUTER MAP ---
functions = {
    "get_pub_ip": get_public_ip, "list_ifaces": list_interfaces, "ping": ping_host,
    "port_scan": scan_port, "dns_settings": get_dns_settings, "flush_dns": flush_dns,
    "arp_table": get_arp_table, "netstat": netstat_view, "dl_file": download_url,
    "check_net": check_internet, "get_host": get_hostname, "get_fqdn": get_fqdn,
    "traceroute": traceroute, "get_gw": get_gateway, "dns_res": resolve_dns,
    "list_wifi": list_wifi, "wifi_disc": disconnect_wifi, "get_routes": get_routing_table,
    "tcp_send": tcp_send, "udp_send": udp_send, "fw_on": enable_firewall,
    "fw_off": disable_firewall, "get_mac": get_mac_address, "tunnel_test": tunnel_test,
    "set_proxy": set_proxy, "unset_proxy": unset_proxy, "port_listen": port_listen,
    "get_speed": get_connection_speed, "ping_gw": ping_gateway, "detect_vpn": detect_vpn
}
