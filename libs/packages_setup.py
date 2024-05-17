# libs/packages_setup.py

import tkinter as tk
from tkinter import ttk, messagebox

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
        self.repos_text = tk.Text(self.frame, height=5, width=50)
        self.repos_text.pack(pady=5)
        self.repos_text.insert(tk.END, "[repo-name]\nSigLevel = Optional TrustAll\nServer = http://example.com/$arch")

        self.suggested_packages_label = ttk.Label(self.frame, text="Suggested Packages for Selected Desktop Environment:")
        self.suggested_packages_label.pack(pady=10)

        self.suggested_packages_text = tk.Text(self.frame, height=5, width=50)
        self.suggested_packages_text.pack(pady=5)

        self.update_suggested_packages()

        self.desktop_env_var.trace("w", self.update_suggested_packages)

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

# Usage example for integration in installer.py:
# packages_frame = ttk.Frame(notebook)
# notebook.add(packages_frame, text="Packages Setup")
# PackagesSetup(packages_frame, desktop_env_var)
