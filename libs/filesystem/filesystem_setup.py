import tkinter as tk
from tkinter import ttk, messagebox
from . import setup_ext4, setup_btrfs, setup_zfs, setup_xfs, setup_jfs, setup_reiserfs, setup_f2fs

class FilesystemSetup:
    def __init__(self, frame):
        self.frame = frame
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.frame, text="Filesystem Setup:").pack(pady=10)

        self.fs_var = tk.StringVar(value="ext4")
        filesystems = ["ext4", "Btrfs", "ZFS", "XFS", "JFS", "ReiserFS", "F2FS"]

        for fs in filesystems:
            ttk.Radiobutton(self.frame, text=fs, variable=self.fs_var, value=fs.lower()).pack(pady=5)

        self.setup_button = ttk.Button(self.frame, text="Setup Filesystem", command=self.setup_filesystem)
        self.setup_button.pack(pady=10)

    def setup_filesystem(self):
        fs = self.fs_var.get()
        if fs == "ext4":
            message = setup_ext4()
        elif fs == "btrfs":
            message = setup_btrfs()
        elif fs == "zfs":
            message = setup_zfs()
        elif fs == "xfs":
            message = setup_xfs()
        elif fs == "jfs":
            message = setup_jfs()
        elif fs == "reiserfs":
            message = setup_reiserfs()
        elif fs == "f2fs":
            message = setup_f2fs()
        else:
            message = "Unknown filesystem selected"

        messagebox.showinfo("Filesystem Setup", message)
