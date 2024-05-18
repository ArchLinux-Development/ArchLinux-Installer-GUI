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
            ttk.Radiobutton(self.frame, text=sw, variable=self.swap_var, value=sw).pack(pady=5)

        self.zram_frame = ttk.Frame(self.frame)
        
        self.zram_size_label = ttk.Label(self.zram_frame, text="ZRAM Size:")
        self.zram_size_label.pack(side="left", padx=5)

        self.zram_size_var = tk.StringVar()
        self.zram_size_combo = ttk.Combobox(self.zram_frame, textvariable=self.zram_size_var, width=10)
        self.zram_size_combo.pack(side="left", padx=5)

        self.populate_zram_sizes()
        self.zram_frame.pack(pady=5)
        print("Initialized SwapSetup and populated ZRAM sizes")

    def populate_zram_sizes(self):
        total_ram_mb = psutil.virtual_memory().total // (1024 * 1024)  # Convert bytes to MB
        zram_sizes_mb = [total_ram_mb // 4, total_ram_mb // 2, total_ram_mb]
        zram_sizes_gb = [f"{size // 1024} GB" for size in zram_sizes_mb]

        self.zram_size_combo['values'] = zram_sizes_gb
        self.zram_size_var.set(zram_sizes_gb[1])  # Default to half of the total RAM
        print(f"ZRAM sizes populated: {zram_sizes_gb}, default: {zram_sizes_gb[1]}")
