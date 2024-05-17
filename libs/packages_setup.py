# libs/packages_setup.py

import tkinter as tk
from tkinter import ttk, messagebox
from .tooltip import ToolTip

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
        # Add the necessary commands for setting up Chaotic-AUR here

    def setup_cachyos_repo(self):
        print("Setting up CachyOS repository inside chroot environment...")
        # Add the necessary commands for setting up CachyOS repository here

# Usage example for integration in installer.py:
# packages_frame = ttk.Frame(notebook)
# notebook.add(packages_frame, text="Packages Setup")
# PackagesSetup(packages_frame, desktop_env_var)
