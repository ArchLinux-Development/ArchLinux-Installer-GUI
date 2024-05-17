# libs/kernel_setup.py

import tkinter as tk
from tkinter import ttk, messagebox

class KernelSetup:
    def __init__(self, frame):
        self.frame = frame
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.frame, text="Kernel Selection:").pack(pady=10)

        self.kernel_var = tk.StringVar(value="linux")

        kernels = [
            "linux (Standard Arch Kernel)",
            "linux-lts (Long Term Support Kernel)",
            "linux-zen (Tuned for desktop performance)",
            "linux-hardened (Security-focused kernel)"
        ]

        for kernel in kernels:
            ttk.Radiobutton(self.frame, text=kernel, variable=self.kernel_var, value=kernel.split()[0]).pack(pady=5)

        self.confirm_button = ttk.Button(self.frame, text="Confirm Kernel Selection", command=self.confirm_selection)
        self.confirm_button.pack(pady=10)

    def confirm_selection(self):
        selected_kernel = self.kernel_var.get()
        messagebox.showinfo("Kernel Selection", f"You have selected: {selected_kernel}")

# Usage example for integration in installer.py:
# kernel_frame = ttk.Frame(notebook)
# notebook.add(kernel_frame, text="Kernel Setup")
# KernelSetup(kernel_frame)
