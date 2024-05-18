# libs/network_setup.py

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess

class NetworkSetup:
    def __init__(self, frame):
        self.frame = frame
        self.network_var = tk.StringVar()
        self.wifi_ssid_var = tk.StringVar()
        self.wifi_password_var = tk.StringVar()
        self.connection_status_var = tk.StringVar(value="Not connected")
        self.create_widgets()
        self.detect_networks()

    def create_widgets(self):
        ttk.Label(self.frame, text="Network Setup:").pack(pady=10)

        self.network_label = ttk.Label(self.frame, text="Network Interface:")
        self.network_label.pack(pady=5)
        self.network_combobox = ttk.Combobox(self.frame, textvariable=self.network_var, state="readonly", width=50)
        self.network_combobox.pack(pady=5)

        self.wifi_label = ttk.Label(self.frame, text="WiFi SSID:")
        self.wifi_label.pack(pady=5)
        self.wifi_combobox = ttk.Combobox(self.frame, textvariable=self.wifi_ssid_var, state="readonly", width=50)
        self.wifi_combobox.pack(pady=5)

        self.wifi_password_label = ttk.Label(self.frame, text="WiFi Password:")
        self.wifi_password_label.pack(pady=5)
        self.wifi_password_entry = ttk.Entry(self.frame, show='*', textvariable=self.wifi_password_var, width=50)
        self.wifi_password_entry.pack(pady=5)

        self.connect_button = ttk.Button(self.frame, text="Connect", command=self.connect_to_network)
        self.connect_button.pack(pady=10)

        self.connection_status_label = ttk.Label(self.frame, textvariable=self.connection_status_var)
        self.connection_status_label.pack(pady=10)

    def detect_networks(self):
        try:
            # Detect network interfaces
            result = subprocess.run(['nmcli', 'device'], stdout=subprocess.PIPE, text=True)
            lines = result.stdout.split('\n')
            interfaces = []
            wifi_interfaces = []
            for line in lines:
                if 'ethernet' in line and 'connected' in line:
                    interfaces.append(line.split()[0])
                elif 'wifi' in line:
                    wifi_interfaces.append(line.split()[0])
                    interfaces.append(line.split()[0])

            if not interfaces:
                self.connection_status_var.set("No network interfaces found")
                return

            self.network_combobox['values'] = interfaces
            self.network_combobox.current(0)
            self.network_var.set(interfaces[0])

            if wifi_interfaces:
                self.detect_wifi_networks(wifi_interfaces[0])
            else:
                self.wifi_combobox['values'] = []
                self.wifi_combobox.set('')

        except Exception as e:
            messagebox.showerror("Error", f"Failed to detect networks: {e}")

    def detect_wifi_networks(self, wifi_interface):
        try:
            # Detect WiFi networks
            result = subprocess.run(['nmcli', 'device', 'wifi', 'list', 'ifname', wifi_interface], stdout=subprocess.PIPE, text=True)
            lines = result.stdout.split('\n')
            ssids = []
            for line in lines[1:]:
                if line:
                    ssid = line.split()[0]
                    ssids.append(ssid)
            
            self.wifi_combobox['values'] = ssids
            if ssids:
                self.wifi_combobox.current(0)
                self.wifi_ssid_var.set(ssids[0])
            else:
                self.wifi_combobox.set('')

        except Exception as e:
            messagebox.showerror("Error", f"Failed to detect WiFi networks: {e}")

    def connect_to_network(self):
        network_interface = self.network_var.get()
        wifi_ssid = self.wifi_ssid_var.get()
        wifi_password = self.wifi_password_var.get()

        if not network_interface:
            messagebox.showerror("Error", "Network interface is required.")
            return

        try:
            # Bring the network interface up
            subprocess.run(['ip', 'link', 'set', network_interface, 'up'], check=True)

            if 'wifi' in network_interface and wifi_ssid:
                # Connect to the WiFi network
                subprocess.run(['nmcli', 'dev', 'wifi', 'connect', wifi_ssid, 'password', wifi_password], check=True)
                self.connection_status_var.set(f"Connected to {wifi_ssid} via WiFi")
            else:
                self.connection_status_var.set(f"Connected via {network_interface}")

            messagebox.showinfo("Success", "Network connected successfully!")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Connection Error", f"Failed to connect to network: {e}")
            self.connection_status_var.set("Connection failed")
