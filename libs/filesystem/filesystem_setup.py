import tkinter as tk
import customtkinter as ctk
import subprocess
from tkinter import messagebox

class FilesystemSetup:
    def __init__(self, frame):
        self.frame = frame
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self.frame, text="Filesystem Setup:").pack(pady=10)

        self.fs_var = tk.StringVar(value="ext4")
        # Added bcachefs, nilfs2, and others as requested
        filesystems = ["ext4", "btrfs", "xfs", "zfs", "f2fs", "bcachefs", "jfs", "reiserfs", "nilfs2"]

        # Grid layout for radio buttons to save space
        self.fs_frame = ctk.CTkFrame(self.frame)
        self.fs_frame.pack(pady=5)
        
        for i, fs in enumerate(filesystems):
            ctk.CTkRadioButton(self.fs_frame, text=fs, variable=self.fs_var, value=fs.lower()).grid(row=i//3, column=i%3, padx=10, pady=5)

        self.device_label = ctk.CTkLabel(self.frame, text="Target Partition:")
        self.device_label.pack(pady=5)
        self.device_combo = ctk.CTkComboBox(self.frame, width=300)
        self.device_combo.pack(pady=5)
        
        self.refresh_btn = ctk.CTkButton(self.frame, text="Refresh Drives", command=self.update_device_list)
        self.refresh_btn.pack(pady=5)

        self.mount_label = ctk.CTkLabel(self.frame, text="Mount Point (e.g. /, /home):")
        self.mount_label.pack(pady=5)
        self.mount_entry = ctk.CTkEntry(self.frame, placeholder_text="/")
        self.mount_entry.pack(pady=5)
        self.mount_entry.insert(0, "/")

        self.update_device_list()

    def update_device_list(self):
        try:
            # -p for full path, -r for raw output to handle spaces better if needed (though text=True handles it ok)
            # We want partitions (part) and disks (disk) potentially
            result = subprocess.run(['lsblk', '-o', 'NAME,SIZE,TYPE,FSTYPE', '-p', '-n', '-r'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0:
                messagebox.showerror("Error", f"Failed to list block devices: {result.stderr}")
                return

            devices = []
            for line in result.stdout.strip().split("\n"):
                if not line: continue
                parts = line.split()
                # parts: NAME SIZE TYPE FSTYPE (optional)
                # We prioritize partitions ('part') but can include disks ('disk') if desired for full wipe
                # users usually install to partitions.
                name = parts[0]
                size = parts[1] if len(parts) > 1 else "?"
                dtype = parts[2] if len(parts) > 2 else "?"
                
                if dtype in ['part', 'disk']:
                    devices.append(f"{name} ({size}) - {dtype}")

            self.device_combo.configure(values=devices)
            if devices:
                self.device_combo.set(devices[0])
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while listing block devices: {str(e)}")

    def get_filesystem_info(self):
        device_selection = self.device_combo.get()
        device_path = device_selection.split()[0] if device_selection else None
        
        return {
            "filesystem": self.fs_var.get(),
            "device": device_path,
            "mount_point": self.mount_entry.get()
        }
