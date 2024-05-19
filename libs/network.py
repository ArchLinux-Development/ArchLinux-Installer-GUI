import subprocess
import socket

def is_connected():
    try:
        socket.create_connection(("8.8.8.8", 53))
        return True
    except OSError:
        return False

def scan_wifi():
    try:
        result = subprocess.run(['nmcli', '-t', '-f', 'SSID', 'device', 'wifi', 'list'], capture_output=True, text=True)
        networks = result.stdout.splitlines()
        return networks
    except Exception as e:
        print(f"Error scanning Wi-Fi networks: {e}")
        return []

def get_interfaces():
    try:
        result = subprocess.run(['nmcli', 'device'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        interfaces = []
        wifi_interfaces = []
        for line in lines:
            if 'ethernet' in line and 'connected' in line:
                interfaces.append(line.split()[0])
            elif 'wifi' in line:
                wifi_interfaces.append(line.split()[0])
                interfaces.append(line.split()[0])
        return interfaces, wifi_interfaces
    except Exception as e:
        print(f"Error getting network interfaces: {e}")
        return [], []
