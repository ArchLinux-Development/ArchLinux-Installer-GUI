import os
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from .tooltip import ToolTip

def is_inside_chroot():
    return os.path.exists("/etc/arch-release") and not os.path.exists("/proc/1/root")

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        return None

class PackagesSetup:
    def __init__(self, frame, desktop_env_var):
        self.frame = frame
        self.desktop_env_var = desktop_env_var
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.frame, text="Additional Packages Setup:").pack(pady=10)

        self.packages_label = ttk.Label(self.frame, text="Extra Packages:")
        self.packages_label.pack(pady=5)
        self.packages_entry = ttk.Entry(self.frame, width=50)
        self.packages_entry.pack(pady=5)
        self.packages_entry.insert(0, "Example: package1 package2 package3")

        self.repos_label = ttk.Label(self.frame, text="Additional Repositories:")
        self.repos_label.pack(pady=5)
        
        self.chaotic_aur_var = tk.BooleanVar()
        self.cachyos_repo_var = tk.BooleanVar()

        self.chaotic_aur_check = ttk.Checkbutton(self.frame, text="Add Chaotic-AUR Repository", variable=self.chaotic_aur_var)
        self.chaotic_aur_check.pack(pady=5)
        
        self.cachyos_repo_check = ttk.Checkbutton(self.frame, text="Add CachyOS Repository", variable=self.cachyos_repo_var)
        self.cachyos_repo_check.pack(pady=5)

        self.suggested_packages_label = ttk.Label(self.frame, text="Suggested Packages for Selected Desktop Environment:")
        self.suggested_packages_label.pack(pady=10)

        self.suggested_packages_text = tk.Text(self.frame, height=5, width=50)
        self.suggested_packages_text.pack(pady=5)

        self.update_suggested_packages()

        self.desktop_env_var.trace("w", self.update_suggested_packages)

        # Add tooltip for CachyOS checkbox
        self.add_tooltip(self.cachyos_repo_check, "Warning: This repository has had issues with package signing keys.")

    def add_tooltip(self, widget, text):
        ToolTip(widget, text)

    def update_suggested_packages(self, *args):
        desktop_env = self.desktop_env_var.get()
        suggested_packages = {
            "gnome": "gnome-tweaks gnome-shell-extensions",
            "kde_plasma": "plasma-wayland-session kdeconnect",
            "xfce": "xfce4-goodies",
            "lxde": "lxappearance",
            "lxqt": "obconf-qt",
            "cinnamon": "cinnamon-translations",
            "mate": "mate-extra",
            "budgie": "budgie-extras",
            "deepin": "deepin-extra",
            "enlightenment": "enlightenment-extra"
        }

        self.suggested_packages_text.delete(1.0, tk.END)
        self.suggested_packages_text.insert(tk.END, suggested_packages.get(desktop_env, "No suggested packages"))

    def confirm_package_selection(self):
        if self.chaotic_aur_var.get():
            self.setup_chaotic_aur()

        if self.cachyos_repo_var.get():
            self.setup_cachyos_repo()

        messagebox.showinfo("Package Setup", "Package setup complete!")

    def setup_chaotic_aur(self):
        print("Setting up Chaotic-AUR inside chroot environment...")
        if not is_inside_chroot():
            print("You are not inside the chroot environment. Please chroot into the system first.")
            return
        run_command("pacman-key --recv-key 3056513887B78AEB --keyserver keyserver.ubuntu.com")
        run_command("pacman-key --lsign-key 3056513887B78AEB")
        run_command("pacman -U 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-keyring.pkg.tar.zst' 'https://cdn-mirror.chaotic.cx/chaotic-aur/chaotic-mirrorlist.pkg.tar.zst'")
        run_command('echo -e "\n[chaotic-aur]\nInclude = /etc/pacman.d/chaotic-mirrorlist" >> /etc/pacman.conf')
        print("Chaotic-AUR setup complete!")

    def setup_cachyos_repo(self):
        print("Setting up CachyOS repository inside chroot environment...")
        if not is_inside_chroot():
            print("You are not inside the chroot environment. Please chroot into the system first.")
            return
        run_command("pacman-key --recv-keys F3B607488DB35A47 --keyserver keyserver.ubuntu.com")
        run_command("pacman-key --lsign-key F3B607488DB35A47")
        run_command("pacman -U 'https://mirror.cachyos.org/repo/x86_64/cachyos/cachyos-keyring-3-1-any.pkg.tar.zst' 'https://mirror.cachyos.org/repo/x86_64/cachyos/cachyos-mirrorlist-17-1-any.pkg.tar.zst' 'https://mirror.cachyos.org/repo/x86_64/cachyos/cachyos-v3-mirrorlist-17-1-any.pkg.tar.zst' 'https://mirror.cachyos.org/repo/x86_64/cachyos/cachyos-v4-mirrorlist-5-1-any.pkg.tar.zst' 'https://mirror.cachyos.org/repo/x86_64/cachyos/pacman-6.0.2-13-x86_64.pkg.tar.zst'")

        cpu_compatibility = run_command("/lib/ld-linux-x86-64.so.2 --help | grep supported | grep x86-64-v4")
        if "supported, searched" in cpu_compatibility.stdout:
            run_command('echo -e "\n[cachyos-v4]\nInclude = /etc/pacman.d/cachyos-v4-mirrorlist" >> /etc/pacman.conf')

        cpu_compatibility_v3 = run_command("/lib/ld-linux-x86-64.so.2 --help | grep supported | grep x86-64-v3")
        if "supported, searched" in cpu_compatibility_v3.stdout:
            run_command('echo -e "\n[cachyos-v3]\nInclude = /etc/pacman.d/cachyos-v3-mirrorlist" >> /etc/pacman.conf')
            run_command('echo -e "\n[cachyos-core-v3]\nInclude = /etc/pacman.d/cachyos-v3-mirrorlist" >> /etc/pacman.conf')
            run_command('echo -e "\n[cachyos-extra-v3]\nInclude = /etc/pacman.d/cachyos-v3-mirrorlist" >> /etc/pacman.conf')

        run_command('echo -e "\n[cachyos]\nInclude = /etc/pacman.d/cachyos-mirrorlist" >> /etc/pacman.conf')
        print("CachyOS repository setup complete!")
