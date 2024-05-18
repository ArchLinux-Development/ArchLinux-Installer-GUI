import tkinter as tk
from tkinter import ttk
import psutil

class SwapSetup:
    def __init__(self, frame):
        self.frame = frame
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.frame, text="Swap Setup:").pack(pady=10)

        self.swap_var = tk.StringVar(value="zram")
        swaps = ["zram", "swap partition", "swap file"]

        for sw in swaps:
            ttk.Radiobutton(self.frame, text=sw, variable=self.swap_var, value=sw, command=self.toggle_zram_options).pack(pady=5)

        self.zram_frame = ttk.Frame(self.frame)
        self.zram_size_label = ttk.Label(self.zram_frame, text="ZRAM Size:")
        self.zram_size_label.pack(side="left", padx=5)

        self.zram_size_var = tk.StringVar()
        self.zram_size_combo = ttk.Combobox(self.zram_frame, textvariable=self.zram_size_var, width=10)
        self.zram_size_combo.pack(side="left", padx=5)

        self.populate_zram_sizes()
        self.toggle_zram_options()

    def populate_zram_sizes(self):
        total_ram = psutil.virtual_memory().total // (1024 * 1024)  # Convert bytes to MB
        zram_sizes = [f"{total_ram // 4} MB", f"{total_ram // 2} MB", f"{total_ram} MB"]

        self.zram_size_combo['values'] = zram_sizes
        self.zram_size_var.set(zram_sizes[1])  # Default to half of the total RAM

    def toggle_zram_options(self):
        if self.swap_var.get() == "zram":
            self.zram_frame.pack(pady=5)
        else:
            self.zram_frame.pack_forget()
