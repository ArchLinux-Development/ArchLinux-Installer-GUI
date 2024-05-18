import tkinter as tk
from tkinter import ttk

class ConfirmationFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        self.confirm_label = ttk.Label(self, text="Review all your settings before proceeding with the installation.", wraplength=600, justify="center")
        self.confirm_label.pack(pady=10)
        
        self.summary_text = tk.Text(self, height=20, width=100, wrap="word")
        self.summary_text.pack(pady=10)

        confirm_button = ttk.Button(self, text="Start Installation", command=self.controller.start_installation)
        confirm_button.pack(pady=10)

    def update_summary(self, user_info, network_info, kernel_info, filesystem_info, bootloader_info, swap_info, desktop_env_info, packages_info):
        self.summary_text.delete(1.0, tk.END)
        summary = (
            f"User Information:\n"
            f"Username: {user_info['username']}\n"
            f"Admin Rights: {user_info['admin_rights']}\n"
            f"Country: {user_info['country']}\n"
            f"Language: {user_info['language']}\n\n"
            f"Network Information:\n{network_info}\n\n"
            f"{kernel_info}\n\n"
            f"{filesystem_info}\n\n"
            f"{bootloader_info}\n\n"
            f"{swap_info}\n\n"
            f"{desktop_env_info}\n\n"
            f"{packages_info}"
        )
        self.summary_text.insert(tk.END, summary)
