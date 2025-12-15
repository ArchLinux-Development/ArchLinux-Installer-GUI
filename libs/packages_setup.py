import os
import subprocess
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
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

def check_package_exists(package_name):
    # Uses pacman -Ss to search. Output is non-empty if found.
    # Alternatively, pacman -Si might be better for exact match, but -Ss is safer for fuzzy or just checking availability.
    # Using -Si returns 0 if found, 1 if not.
    try:
        subprocess.run(f"pacman -Si {package_name}", shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

class PackagesSetup:
    def __init__(self, frame, desktop_env_var):
        self.frame = frame
        self.desktop_env_var = desktop_env_var
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self.frame, text="Additional Packages Setup:").pack(pady=10)

        self.packages_label = ctk.CTkLabel(self.frame, text="Extra Packages (Space separated):")
        self.packages_label.pack(pady=5)
        
        # Using a frame for entry and validate button
        self.pkg_input_frame = ctk.CTkFrame(self.frame)
        self.pkg_input_frame.pack(pady=5)
        
        self.packages_entry = ctk.CTkEntry(self.pkg_input_frame, width=300)
        self.packages_entry.pack(side="left", padx=5)
        
        self.validate_btn = ctk.CTkButton(self.pkg_input_frame, text="Validate", width=80, command=self.validate_packages)
        self.validate_btn.pack(side="left", padx=5)
        
        self.validation_label = ctk.CTkLabel(self.frame, text="", text_color="gray")
        self.validation_label.pack(pady=2)

        self.repos_label = ctk.CTkLabel(self.frame, text="Additional Repositories:")
        self.repos_label.pack(pady=5)
        
        self.chaotic_aur_var = tk.BooleanVar()
        self.cachyos_repo_var = tk.BooleanVar()

        self.chaotic_aur_check = ctk.CTkCheckBox(self.frame, text="Add Chaotic-AUR Repository", variable=self.chaotic_aur_var)
        self.chaotic_aur_check.pack(pady=5)
        
        self.cachyos_repo_check = ctk.CTkCheckBox(self.frame, text="Add CachyOS Repository", variable=self.cachyos_repo_var)
        self.cachyos_repo_check.pack(pady=5)

        self.suggested_packages_label = ctk.CTkLabel(self.frame, text="Suggested Packages for Selected Desktop Environment:")
        self.suggested_packages_label.pack(pady=10)

        self.suggested_packages_text = ctk.CTkTextbox(self.frame, height=100, width=400)
        self.suggested_packages_text.pack(pady=5)

        self.update_suggested_packages()

        self.desktop_env_var.trace("w", self.update_suggested_packages)

        # Add tooltip for CachyOS checkbox
        self.add_tooltip(self.cachyos_repo_check, "Warning: This repository has had issues with package signing keys.")

    def add_tooltip(self, widget, text):
        ToolTip(widget, text)

    def update_suggested_packages(self, *args): # pylint: disable=unused-argument
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

        self.suggested_packages_text.delete("0.0", "end")
        self.suggested_packages_text.insert("0.0", suggested_packages.get(desktop_env, "No suggested packages"))

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
        run_command('echo -e "\n[cachyos]\nInclude = /etc/pacman.d/cachyos-mirrorlist" >> /etc/pacman.conf')
        print("CachyOS repository setup complete!")

    def validate_packages(self):
        pkg_str = self.packages_entry.get()
        if not pkg_str.strip():
            self.validation_label.configure(text="No packages entered", text_color="yellow")
            return

        packages = pkg_str.split()
        invalid_pkgs = []
        valid_pkgs = []
        
        for pkg in packages:
             if check_package_exists(pkg):
                 valid_pkgs.append(pkg)
             else:
                 invalid_pkgs.append(pkg)
        
        if invalid_pkgs:
            self.validation_label.configure(text=f"Invalid: {', '.join(invalid_pkgs)}", text_color="red")
            messagebox.showwarning("Package Validation", f"The following packages were not found in repositories:\n{', '.join(invalid_pkgs)}")
        else:
            self.validation_label.configure(text="All packages valid!", text_color="green")
            messagebox.showinfo("Package Validation", "All packages verified successfully.")
