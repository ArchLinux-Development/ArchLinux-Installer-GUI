import tkinter as tk
from tkinter import ttk, messagebox
import subprocess

class NetworkSetup:
    def __init__(self, frame):
        self.frame = frame
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.frame, text="Network Setup:").pack(pady=10)

        self.check_network_button = ttk.Button(self.frame, text="Check Network", command=self.check_network)
        self.check_network_button.pack(pady=5)

        self.scan_wifi_button = ttk.Button(self.frame, text="Scan for Wi-Fi Networks", command=self.scan_wifi)
        self.scan_wifi_button.pack(pady=5)

        self.wifi_ssid_label = ttk.Label(self.frame, text="Wi-Fi SSID:")
        self.wifi_ssid_label.pack(pady=5)

        self.wifi_ssid_combo = ttk.Combobox(self.frame)
        self.wifi_ssid_combo.pack(pady=5)

        self.wifi_password_label = ttk.Label(self.frame, text="Wi-Fi Password:")
        self.wifi_password_label.pack(pady=5)
        self.wifi_password_entry = ttk.Entry(self.frame, show="*")
        self.wifi_password_entry.pack(pady=5)

        self.connect_wifi_button = ttk.Button(self.frame, text="Connect to Wi-Fi", command=self.connect_wifi)
        self.connect_wifi_button.pack(pady=5)

    def check_network(self):
        try:
            result = subprocess.run(['ping', '-c', '1', '8.8.8.8'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                messagebox.showinfo("Network Check", "Network is connected")
            else:
                messagebox.showwarning("Network Check", "Network is not connected. Please connect to Wi-Fi.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while checking the network: {str(e)}")

    def scan_wifi(self):
        try:
            result = subprocess.run(['nmcli', '-t', '-f', 'SSID', 'dev', 'wifi'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                wifi_list = result.stdout.decode().splitlines()
                self.wifi_ssid_combo['values'] = wifi_list
                messagebox.showinfo("Wi-Fi Scan", "Wi-Fi networks found")
            else:
                messagebox.showerror("Wi-Fi Scan", f"Failed to scan for Wi-Fi networks: {result.stderr.decode()}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while scanning for Wi-Fi networks: {str(e)}")

    def connect_wifi(self):
        ssid = self.wifi_ssid_combo.get()
        password = self.wifi_password_entry.get()
        
        if not ssid or not password:
            messagebox.showwarning("Input Error", "Please enter both SSID and password")
            return

        try:
            result = subprocess.run(['nmcli', 'dev', 'wifi', 'connect', ssid, 'password', password], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                messagebox.showinfo("Wi-Fi Connection", "Successfully connected to Wi-Fi")
            else:
                messagebox.showerror("Wi-Fi Connection", f"Failed to connect to Wi-Fi: {result.stderr.decode()}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while connecting to Wi-Fi: {str(e)}")
