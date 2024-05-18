import tkinter as tk
from tkinter import ttk

class PackagesSetupFrame(ttk.Frame):
    def __init__(self, parent, desktop_env_var):
        super().__init__(parent)
        self.desktop_env_var = desktop_env_var
        self.create_widgets()

    def create_widgets(self):
        # Add packages setup widgets here
        ttk.Label(self, text="Packages Setup").pack(pady=5)
        self.chaotic_aur_var = tk.BooleanVar()
        ttk.Checkbutton(self, text="Enable Chaotic AUR", variable=self.chaotic_aur_var).pack(pady=5)
        
        self.cachyos_repo_var = tk.BooleanVar()
        ttk.Checkbutton(self, text="Enable CachyOS Repo", variable=self.cachyos_repo_var).pack(pady=5)

    def setup_chaotic_aur(self):
        print("Setting up Chaotic AUR...")

    def setup_cachyos_repo(self):
        print("Setting up CachyOS Repo...")
