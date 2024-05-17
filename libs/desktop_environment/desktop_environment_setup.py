# libs/desktop_environment_setup.py

import tkinter as tk
from tkinter import ttk, messagebox

class DesktopEnvironmentSetup:
    def __init__(self, frame, desktop_env_var):
        self.frame = frame
        self.desktop_env_var = desktop_env_var
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.frame, text="Desktop Environment Setup:").pack(pady=10)

        self.desktop_env_var.set("gnome")  # Default desktop environment
        environments = ["gnome", "kde_plasma", "xfce", "lxde", "lxqt", "cinnamon", "mate", "budgie", "deepin", "enlightenment"]

        self.env_menu = ttk.OptionMenu(self.frame, self.desktop_env_var, environments[0], *environments)
        self.env_menu.pack(pady=5)

        self.xorg_var = tk.BooleanVar(value=True)
        self.wayland_var = tk.BooleanVar(value=False)

        self.xorg_check = ttk.Checkbutton(self.frame, text="Install Xorg", variable=self.xorg_var)
        self.xorg_check.pack(pady=5)

        self.wayland_check = ttk.Checkbutton(self.frame, text="Install Wayland", variable=self.wayland_var)
        self.wayland_check.pack(pady=5)

        self.info_label = ttk.Label(self.frame, text="Select at least one: Xorg or Wayland.")
        self.info_label.pack(pady=5)

    def validate_selection(self):
        if not self.xorg_var.get() and not self.wayland_var.get():
            messagebox.showerror("Selection Error", "You must select at least one: Xorg or Wayland.")
            return False
        return True
