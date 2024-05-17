# libs/user_input.py

import tkinter as tk
from tkinter import ttk
import psutil
import platform
import subprocess
import locale

class UserInput:
    def __init__(self, frame):
        self.frame = frame
        self.create_widgets()
        self.detect_locale()

    def create_widgets(self):
        ttk.Label(self.frame, text="User Information:").pack(pady=10)

        ttk.Label(self.frame, text="Username:").pack(pady=5)
        self.username_entry = ttk.Entry(self.frame, width=50)
        self.username_entry.pack(pady=5)

        ttk.Label(self.frame, text="Password:").pack(pady=5)
        self.password_entry = ttk.Entry(self.frame, show='*', width=50)
        self.password_entry.pack(pady=5)

        ttk.Label(self.frame, text="Admin Password:").pack(pady=5)
        self.admin_password_entry = ttk.Entry(self.frame, show='*', width=50)
        self.admin_password_entry.pack(pady=5)

        self.admin_rights_var = tk.BooleanVar(value=True)
        self.admin_rights_check = ttk.Checkbutton(self.frame, text="Grant admin rights", variable=self.admin_rights_var)
        self.admin_rights_check.pack(pady=5)

        ttk.Label(self.frame, text="Locale Settings:").pack(pady=10)

        ttk.Label(self.frame, text="Country:").pack(pady=5)
        self.country_var = tk.StringVar()
        self.country_combobox = ttk.Combobox(self.frame, textvariable=self.country_var, width=47)
        self.country_combobox.pack(pady=5)

        ttk.Label(self.frame, text="Language:").pack(pady=5)
        self.language_var = tk.StringVar()
        self.language_combobox = ttk.Combobox(self.frame, textvariable=self.language_var, width=47)
        self.language_combobox.pack(pady=5)

        ttk.Label(self.frame, text="Hardware Detection:").pack(pady=10)
        self.detect_hardware_button = ttk.Button(self.frame, text="Detect Hardware", command=self.detect_hardware)
        self.detect_hardware_button.pack(pady=5)

        self.hardware_text = tk.Text(self.frame, height=10, width=80)
        self.hardware_text.pack(pady=5)

    def detect_locale(self):
        # Detect current locale
        current_locale = locale.getdefaultlocale()
        print(f"Detected locale: {current_locale}")

        if current_locale and current_locale[0]:
            try:
                current_language, current_country = current_locale[0].split('_')
            except ValueError:
                current_language, current_country = 'en', 'US'  # Fallback defaults
        else:
            current_language, current_country = 'en', 'US'  # Default to English and US if detection fails

        print(f"Detected language: {current_language}, country: {current_country}")

        # Populate comboboxes with options
        countries = ['US', 'GB', 'FR', 'DE', 'ES', 'IT', 'CN', 'JP']  # Add more countries as needed
        languages = ['en', 'fr', 'de', 'es', 'it', 'zh', 'ja']  # Add more languages as needed

        if current_country not in countries:
            countries.insert(0, current_country)
        if current_language not in languages:
            languages.insert(0, current_language)

        self.country_combobox['values'] = countries
        self.language_combobox['values'] = languages

        # Set comboboxes with detected locale
        self.country_combobox.set(current_country)
        self.language_combobox.set(current_language)

    def detect_hardware(self):
        self.hardware_text.delete(1.0, tk.END)
        cpu_info = platform.processor()
        memory_info = psutil.virtual_memory()
        gpu_info = self.detect_gpu()

        self.hardware_text.insert(tk.END, f"CPU: {cpu_info}\n")
        self.hardware_text.insert(tk.END, f"Memory: {memory_info.total / (1024 ** 3):.2f} GB\n")
        self.hardware_text.insert(tk.END, f"GPU: {gpu_info}\n")

    def detect_gpu(self):
        try:
            result = subprocess.run(['lspci'], stdout=subprocess.PIPE, text=True)
            lines = result.stdout.split('\n')
            for line in lines:
                if 'VGA' in line or '3D' in line:
                    return line
            return "No GPU found"
        except Exception as e:
            return f"Error detecting GPU: {e}"

    def get_user_info(self):
        return {
            'username': self.username_entry.get(),
            'password': self.password_entry.get(),
            'admin_password': self.admin_password_entry.get(),
            'admin_rights': self.admin_rights_var.get(),
            'country': self.country_var.get(),
            'language': self.language_var.get(),
        }
