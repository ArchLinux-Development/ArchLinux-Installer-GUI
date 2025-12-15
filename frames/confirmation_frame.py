import customtkinter as ctk
import tkinter as tk

class ConfirmationFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        self.confirm_label = ctk.CTkLabel(self, text="Review all your settings before proceeding with the installation.", wraplength=600, justify="center")
        self.confirm_label.pack(pady=10)
        
        self.summary_text = ctk.CTkTextbox(self, height=400, width=800, wrap="word")
        self.summary_text.pack(pady=10)

        self.save_btn = ctk.CTkButton(self, text="Save Configuration", command=self.controller.save_configuration)
        self.save_btn.pack(pady=10)

    def update_summary(self, user_info, network_info, kernel_info, filesystem_info, bootloader_info, swap_info, desktop_env_info, packages_info):
        self.summary_text.delete("0.0", "end")
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
        self.summary_text.insert("0.0", summary)
