import customtkinter as ctk
import tkinter as tk

class InstallationProgressFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        self.label = ctk.CTkLabel(self, text="Installation in Progress", font=("Roboto", 20))
        self.label.pack(pady=20)

        self.console_textbox = ctk.CTkTextbox(self, width=800, height=500, font=("Courier", 12))
        self.console_textbox.pack(pady=10, padx=10, fill="both", expand=True)
        self.console_textbox.configure(state="disabled")

    def append_text(self, text):
        self.console_textbox.configure(state="normal")
        self.console_textbox.insert("end", text)
        self.console_textbox.see("end")
        self.console_textbox.configure(state="disabled")
