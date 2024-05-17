import tkinter as tk
from tkinter import ttk

class UserInput:
    def __init__(self, frame):
        self.frame = frame
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.frame, text="Enter your user information:").pack(pady=10)

        self.username_label = ttk.Label(self.frame, text="Username:")
        self.username_label.pack(pady=5)
        self.username_entry = ttk.Entry(self.frame)
        self.username_entry.pack(pady=5)

        self.password_label = ttk.Label(self.frame, text="Password:")
        self.password_label.pack(pady=5)
        self.password_entry = ttk.Entry(self.frame, show="*")
        self.password_entry.pack(pady=5)

        self.admin_password_label = ttk.Label(self.frame, text="Admin Password:")
        self.admin_password_label.pack(pady=5)
        self.admin_password_entry = ttk.Entry(self.frame, show="*")
        self.admin_password_entry.pack(pady=5)
