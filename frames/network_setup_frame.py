import tkinter as tk
from tkinter import ttk, messagebox
from libs import network

class NetworkSetupFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.pack(fill=tk.BOTH, expand=True)
        self.network_var = tk.StringVar()
        self.wifi_ssid_var = tk.StringVar()
        self.wifi_password_var = tk.StringVar()
        self.connection_status_var = tk.StringVar(value="Checking network status...")
        self.create_widgets()
        self.update_network_status()
        self.detect_networks()

    def create_widgets(self):
        ttk.Label(self, text="Network Setup:").pack(pady=10)

        self.network_label = ttk.Label(self, text="Network Interface:")
        self.network_label.pack(pady=5)
        self.network_combobox = ttk.Combobox(self, textvariable=self.network_var, state="readonly", width=50)
        self.network_combobox.pack(pady=5)

        self.wifi_label = ttk.Label(self, text="WiFi SSID:")
        self.wifi_label.pack(pady=5)
        self.wifi_combobox = ttk.Combobox(self, textvariable=self.wifi_ssid_var, state="readonly", width=50)
        self.wifi_combobox.pack(pady=5)

        self.wifi_password_label = ttk.Label(self, text="WiFi Password:")
        self.wifi_password_label.pack(pady=5)
        self.wifi_password_entry = ttk.Entry(self, show='*', textvariable=self.wifi_password_var, width=50)
        self.wifi_password_entry.pack(pady=5)

        self.connect_button = ttk.Button(self, text="Connect", command=self.connect_to_network)
        self.connect_button.pack(pady=10)

        self.connection_status_label = ttk.Label(self, textvariable=self.connection_status_var)
        self.connection_status_label.pack(pady=10)

    def update_network_status(self):
        if network.is_connected():
            self.connection_status_var.set("Connected to the internet")
        else:
            self.connection_status_var.set("Not connected to the internet")

    def detect_networks(self):
        interfaces, wifi_interfaces = network.get_interfaces()
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

    def detect_wifi_networks(self, wifi_interface):
        networks = network.scan_wifi()
        self.wifi_combobox['values'] = networks
        if networks:
            self.wifi_combobox.current(0)
            self.wifi_ssid_var.set(networks[0])
        else:
            self.wifi_combobox.set('')

    def connect_to_network(self):
        network_interface = self.network_var.get()
        wifi_ssid = self.wifi_ssid_var.get()
        wifi_password = self.wifi_password_var.get()

        if not network_interface:
            messagebox.showerror("Error", "Network interface is required.")
            return

        try:
            subprocess.run(['ip', 'link', 'set', network_interface, 'up'], check=True)
            if 'wifi' in network_interface and wifi_ssid:
                subprocess.run(['nmcli', 'dev', 'wifi', 'connect', wifi_ssid, 'password', wifi_password], check=True)
                self.connection_status_var.set(f"Connected to {wifi_ssid} via WiFi")
            else:
                self.connection_status_var.set(f"Connected via {network_interface}")

            messagebox.showinfo("Success", "Network connected successfully!")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Connection Error", f"Failed to connect to network: {e}")
            self.connection_status_var.set("Connection failed")

    def get_network_info(self):
        return {
            'interface': self.network_var.get(),
            'status': self.connection_status_var.get(),
            'wifi_ssid': self.wifi_ssid_var.get()
        }

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Network Setup")
    frame = NetworkSetupFrame(root)
    root.mainloop()
