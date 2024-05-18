import tkinter as tk
from tkinter import ttk

class BootloaderSetupFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self, text="Bootloader Setup").pack(pady=5)
        ttk.Label(self, text="Select Bootloader:").pack(pady=5)

        self.bootloader_var = tk.StringVar()
        self.bootloader_combo = ttk.Combobox(self, textvariable=self.bootloader_var)
        self.bootloader_combo.pack(pady=5)
        self.bootloader_combo['values'] = ["GRUB", "systemd-boot", "rEFInd"]
        self.bootloader_combo.current(0)
