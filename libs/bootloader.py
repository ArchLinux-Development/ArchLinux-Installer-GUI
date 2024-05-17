import tkinter as tk
from tkinter import ttk

class BootloaderSetup:
    def __init__(self, frame):
        self.frame = frame
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.frame, text="Bootloader Setup:").pack(pady=10)

        self.bootloader_var = tk.StringVar(value="grub")
        bootloaders = ["grub", "systemd-boot"]

        for bl in bootloaders:
            ttk.Radiobutton(self.frame, text=bl, variable=self.bootloader_var, value=bl).pack(pady=5)
