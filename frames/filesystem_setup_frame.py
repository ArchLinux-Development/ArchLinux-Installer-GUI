import tkinter as tk
from tkinter import ttk
from libs.filesystem.filesystem_setup import FilesystemSetup

class FilesystemSetupFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.filesystem_setup = FilesystemSetup(self)

    def get_filesystem_info(self):
        return {
            "selected_filesystem": self.filesystem_setup.fs_var.get(),
            "selected_device": self.filesystem_setup.device_combo.get()
        }
