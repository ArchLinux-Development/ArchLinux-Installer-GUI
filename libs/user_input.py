# libs/user_input.py

import tkinter as tk
from tkinter import ttk

class UserInput:
    def __init__(self, frame):
        self.frame = frame
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.frame, text="User Information:").pack(pady=10)

        ttk.Label(self.frame, text="Username:").pack(pady=5)
        self.username_entry = ttk.Entry(self.frame, width=50)
        self.username_entry.pack(pady=5)

        ttk.Label(self.frame, text="Password:").pack(pady=5)
        self.password_entry = ttk.Entry(self.frame, show='*', width=50)
        self.password_entry.pack(pady=5)

        self.admin_rights_var = tk.BooleanVar(value=True)
        self.admin_rights_check = ttk.Checkbutton(self.frame, text="Grant admin rights", variable=self.admin_rights_var)
        self.admin_rights_check.pack(pady=5)

    def get_user_info(self):
        return {
            'username': self.username_entry.get(),
            'password': self.password_entry.get(),
            'admin_rights': self.admin_rights_var.get()
        }

# Usage example for integration in installer.py:
# user_input_frame = ttk.Frame(notebook)
# notebook.add(user_input_frame, text="User Input")
# user_input = UserInput(user_input_frame)
