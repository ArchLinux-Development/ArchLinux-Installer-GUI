import tkinter as tk
import customtkinter as ctk
import psutil

class SwapSetup:
    def __init__(self, frame):
        self.frame = frame
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self.frame, text="Swap Setup:").pack(pady=10)

        self.swap_var = tk.StringVar(value="zram")
        swaps = ["zram", "swap partition", "swap file"]

        for sw in swaps:
            ctk.CTkRadioButton(self.frame, text=sw, variable=self.swap_var, value=sw).pack(pady=5)

        self.zram_frame = ctk.CTkFrame(self.frame)

        self.zram_size_label = ctk.CTkLabel(self.zram_frame, text="ZRAM Size:")
        self.zram_size_label.pack(side="left", padx=5)

        self.zram_size_var = tk.StringVar()
        self.zram_size_combo = ctk.CTkComboBox(self.zram_frame, variable=self.zram_size_var, width=200)
        self.zram_size_combo.pack(side="left", padx=5)

        self.populate_zram_sizes()
        self.zram_frame.pack(pady=5)

    def populate_zram_sizes(self):
        total_ram_mb = psutil.virtual_memory().total // (1024 * 1024)  # Convert bytes to MB
        half_ram_mb = total_ram_mb // 2
        zram_sizes_mb = [total_ram_mb // 4, half_ram_mb, total_ram_mb]
        zram_sizes_gb = [f"{size // 1024} GB ({size} MB)" for size in zram_sizes_mb]

        self.zram_size_combo['values'] = zram_sizes_gb
        self.zram_size_var.set(zram_sizes_gb[1])  # Default to half of the total RAM
        self.zram_size_combo.current(1)  # Set the default selection in the combo box

        print(f"ZRAM sizes populated: {zram_sizes_gb}, default: {zram_sizes_gb[1]}")
