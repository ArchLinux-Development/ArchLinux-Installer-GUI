import tkinter as tk
from tkinter import ttk
import subprocess

class NetworkSetupFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Network Interface:").pack(pady=5)
        self.network_var = tk.StringVar()
        self.network_combo = ttk.Combobox(self, textvariable=self.network_var)
        self.network_combo.pack(pady=5)
        self.detect_network_interfaces()

        ttk.Label(self, text="WiFi SSID:").pack(pady=5)
        self.wifi_ssid_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.wifi_ssid_var).pack(pady=5)

        ttk.Label(self, text="Connection Status:").pack(pady=5)
        self.connection_status_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.connection_status_var).pack(pady=5)

    def detect_network_interfaces(self):
        # Detect network interfaces (mocked for simplicity)
        interfaces = ["eth0", "wlan0", "lo"]
        self.network_combo['values'] = interfaces
        if interfaces:
            self.network_combo.current(0)

    def get_network_info(self):
        return f"Network Interface: {self.network_var.get()}\nWiFi SSID: {self.wifi_ssid_var.get()}\nConnection Status: {self.connection_status_var.get()}"
