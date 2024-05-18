import tkinter as tk
from tkinter import ttk
from libs.kernel_setup import KernelSetup

class KernelSetupFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.kernel_setup = KernelSetup(self)

    def get_kernel_info(self):
        return {
            "selected_kernel": self.kernel_setup.kernel_var.get()
        }
