import tkinter as tk
from tkinter import ttk

class UserInputFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        # Add user input widgets here
        ttk.Label(self, text="Username:").pack(pady=5)
        self.username_entry = ttk.Entry(self)
        self.username_entry.pack(pady=5)

        ttk.Label(self, text="Admin Rights:").pack(pady=5)
        self.admin_rights_var = tk.BooleanVar()
        ttk.Checkbutton(self, variable=self.admin_rights_var).pack(pady=5)

        ttk.Label(self, text="Country:").pack(pady=5)
        self.country_entry = ttk.Entry(self)
        self.country_entry.pack(pady=5)

        ttk.Label(self, text="Language:").pack(pady=5)
        self.language_entry = ttk.Entry(self)
        self.language_entry.pack(pady=5)

    def get_user_info(self):
        return {
            "username": self.username_entry.get(),
            "admin_rights": self.admin_rights_var.get(),
            "country": self.country_entry.get(),
            "language": self.language_entry.get(),
        }
