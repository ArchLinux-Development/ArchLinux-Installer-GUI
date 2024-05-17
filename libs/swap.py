import tkinter as tk
from tkinter import ttk

class SwapSetup:
    def __init__(self, frame):
        self.frame = frame
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.frame, text="Swap Setup:").pack(pady=10)

        self.swap_var = tk.StringVar(value="zram")
        swaps = ["zram", "swap partition", "swap file"]

        for sw in swaps:
            ttk.Radiobutton(self.frame, text=sw, variable=self.swap_var, value=sw).pack(pady=5)
