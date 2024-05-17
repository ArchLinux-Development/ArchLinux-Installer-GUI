import tkinter as tk
from tkinter import ttk

class FilesystemSetup:
    def __init__(self, frame):
        self.frame = frame
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.frame, text="Filesystem Setup:").pack(pady=10)

        self.filesystem_var = tk.StringVar(value="ext4")
        filesystems = ["ext4", "btrfs", "zfs"]

        for fs in filesystems:
            ttk.Radiobutton(self.frame, text=fs, variable=self.filesystem_var, value=fs).pack(pady=5)

        self.compression_var = tk.BooleanVar()
        self.compression_check = ttk.Checkbutton(self.frame, text="Enable Compression (BTRFS only)", variable=self.compression_var)
        self.compression_check.pack(pady=5)
