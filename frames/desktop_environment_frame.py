import tkinter as tk
from tkinter import ttk
from libs.desktop_environment.desktop_environment_setup import DesktopEnvironmentSetup

class DesktopEnvironmentFrame(ttk.Frame):
    def __init__(self, parent, desktop_env_var):
        super().__init__(parent)
        self.desktop_env_var = desktop_env_var
        self.desktop_environment_setup = DesktopEnvironmentSetup(self, desktop_env_var)

    def get_desktop_env_info(self):
        return {
            "desktop_environment": self.desktop_environment_setup.desktop_env_var.get(),
            "xorg": self.desktop_environment_setup.xorg_var.get(),
            "wayland": self.desktop_environment_setup.wayland_var.get(),
        }

    def validate_selection(self):
        return self.desktop_environment_setup.validate_selection()
