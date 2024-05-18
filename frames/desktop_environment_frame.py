import tkinter as tk
from tkinter import ttk

class DesktopEnvironmentFrame(ttk.Frame):
    def __init__(self, parent, desktop_env_var):
        super().__init__(parent)
        self.desktop_env_var = desktop_env_var
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Desktop Environment Setup").pack(pady=5)
        ttk.Label(self, text="Select Desktop Environment:").pack(pady=5)

        self.desktop_env_combo = ttk.Combobox(self, textvariable=self.desktop_env_var)
        self.desktop_env_combo.pack(pady=5)
        self.desktop_env_combo['values'] = ["GNOME", "KDE Plasma", "XFCE", "LXQt", "MATE", "Cinnamon"]
        self.desktop_env_combo.current(0)

        self.xorg_var = tk.BooleanVar()
        ttk.Checkbutton(self, text="Install Xorg", variable=self.xorg_var).pack(pady=5)

        self.wayland_var = tk.BooleanVar()
        ttk.Checkbutton(self, text="Install Wayland", variable=self.wayland_var).pack(pady=5)

    def get_desktop_env_info(self):
        return f"Desktop Environment: {self.desktop_env_var.get()}\nXorg: {self.xorg_var.get()}\nWayland: {self.wayland_var.get()}"

    def validate_selection(self):
        if not self.desktop_env_var.get():
            tk.messagebox.showerror("Error", "Please select a desktop environment.")
            return False
        return True
