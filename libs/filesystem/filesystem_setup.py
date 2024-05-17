import tkinter as tk
from tkinter import ttk, messagebox
from . import setup_ext4, setup_btrfs, setup_zfs, setup_xfs, setup_jfs, setup_reiserfs, setup_f2fs
import subprocess

class FilesystemSetup:
    def __init__(self, frame):
        self.frame = frame
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.frame, text="Filesystem Setup:").pack(pady=10)

        self.fs_var = tk.StringVar(value="ext4")
        filesystems = ["ext4", "Btrfs", "ZFS", "XFS", "JFS", "ReiserFS", "F2FS"]

        for fs in filesystems:
            ttk.Radiobutton(self.frame, text=fs, variable=self.fs_var, value=fs.lower()).pack(pady=5)

        self.device_label = ttk.Label(self.frame, text="Device:")
        self.device_label.pack(pady=5)
        self.device_combo = ttk.Combobox(self.frame)
        self.device_combo.pack(pady=5)
        self.update_device_list()

        self.setup_button = ttk.Button(self.frame, text="Setup Filesystem", command=self.setup_filesystem)
        self.setup_button.pack(pady=10)

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

    def setup_filesystem(self):
        fs = self.fs_var.get()
        device = self.device_combo.get().split()[0]
        mount_point = "/mnt"  # Default mount point

        if not device:
            messagebox.showwarning("Input Error", "Please select a device")
            return

        if fs == "ext4":
            message = setup_ext4(device)
        elif fs == "btrfs":
            message = setup_btrfs(device)
        elif fs == "zfs":
            message = setup_zfs(device)
        elif fs == "xfs":
            message = setup_xfs(device)
        elif fs == "jfs":
            message = setup_jfs(device)
        elif fs == "reiserfs":
            message = setup_reiserfs(device)
        elif fs == "f2fs":
            message = setup_f2fs(device)
        else:
            message = "Unknown filesystem selected"

        if "successfully" in message:
            self.run_pacstrap(device, mount_point)
        
        messagebox.showinfo("Filesystem Setup", message)

    def run_pacstrap(self, device, mount_point):
        try:
            # Mount the root filesystem and run pacstrap
            subprocess.run(['mount', device, mount_point], check=True)
            subprocess.run(['pacstrap', mount_point, 'base', 'base-devel'], check=True)
            subprocess.run(['genfstab', '-U', mount_point, '>', f'{mount_point}/etc/fstab'], shell=True, check=True)
            
            # Chroot into the new system to install additional packages
            subprocess.run(['arch-chroot', mount_point, 'bash', '-c', 'pacman -S grub'], check=True)
            subprocess.run(['arch-chroot', mount_point, 'grub-install', device], check=True)
            subprocess.run(['arch-chroot', mount_point, 'grub-mkconfig', '-o', '/boot/grub/grub.cfg'], check=True)
            
            messagebox.showinfo("Pacstrap", "Base system and bootloader installed successfully")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Pacstrap Error", f"Error during installation: {e}")
