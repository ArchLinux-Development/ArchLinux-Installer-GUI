import tkinter as tk
from tkinter import ttk
from libs.packages_setup import PackagesSetup

class PackagesSetupFrame(ttk.Frame):
    def __init__(self, parent, desktop_env_var):
        super().__init__(parent)
        self.packages_setup = PackagesSetup(self, desktop_env_var)

    def get_packages_info(self):
        return {
            "extra_packages": self.packages_setup.packages_entry.get(),
            "chaotic_aur": self.packages_setup.chaotic_aur_var.get(),
            "cachyos_repo": self.packages_setup.cachyos_repo_var.get(),
        }
