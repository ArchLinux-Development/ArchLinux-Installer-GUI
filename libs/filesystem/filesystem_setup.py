import tkinter as tk
from tkinter import ttk
import subprocess
from tkinter import messagebox

class FilesystemSetup:
    def __init__(self, frame):
        self.frame = frame
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.frame, text="Filesystem Setup:").pack(pady=10)

        self.fs_var = tk.StringVar(value="ext4")
        filesystems = ["ext4", "btrfs", "zfs", "xfs", "jfs", "reiserfs", "f2fs"]

        for fs in filesystems:
            ttk.Radiobutton(self.frame, text=fs, variable=self.fs_var, value=fs.lower()).pack(pady=5)

        self.device_label = ttk.Label(self.frame, text="Device:")
        self.device_label.pack(pady=5)
        self.device_combo = ttk.Combobox(self.frame)
        self.device_combo.pack(pady=5)
        self.update_device_list()

    def update_device_list(self):
        try:
            result = subprocess.run(['lsblk', '-o', 'NAME,SIZE,TYPE,MOUNTPOINT', '-n', '-d'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                messagebox.showerror("Error", f"Failed to list block devices: {result.stderr}")
                return

            devices = []
            for line in result.stdout.strip().split("\n"):
                parts = line.split()
                if len(parts) >= 2 and parts[2] == 'disk':
                    devices.append(f"/dev/{parts[0]} ({parts[1]})")

            self.device_combo['values'] = devices
            if devices:
                self.device_combo.current(0)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while listing block devices: {str(e)}")

    def get_filesystem_info(self):
        return {
            "filesystem": self.fs_var.get(),
            "device": self.device_combo.get().split()[0] if self.device_combo.get() else None
        }
