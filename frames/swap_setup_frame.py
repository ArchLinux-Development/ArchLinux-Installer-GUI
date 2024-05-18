import tkinter as tk
from tkinter import ttk
from libs.swap import SwapSetup

class SwapSetupFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.swap_setup = SwapSetup(self)

    def get_swap_info(self):
        return {
            "selected_swap": self.swap_setup.swap_var.get(),
            "zram_size": self.swap_setup.zram_size_var.get() if self.swap_setup.swap_var.get() == "zram" else None
        }
