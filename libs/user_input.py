import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
from tkinter.scrolledtext import ScrolledText

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

        ttk.Label(self.frame, text="Choose your country:").pack(pady=10)
        self.country_combo = ttk.Combobox(self.frame)
        self.country_combo.pack(pady=5)
        self.update_country_list()

        ttk.Label(self.frame, text="Choose your language:").pack(pady=10)
        self.language_combo = ttk.Combobox(self.frame)
        self.language_combo.pack(pady=5)
        self.update_language_list()

        ttk.Label(self.frame, text="Choose your locale:").pack(pady=10)
        self.locale_combo = ttk.Combobox(self.frame)
        self.locale_combo.pack(pady=5)
        self.update_locale_list()

        self.detect_hardware_button = ttk.Button(self.frame, text="Detect Hardware", command=self.detect_hardware)
        self.detect_hardware_button.pack(pady=10)

        self.hardware_info_text = ScrolledText(self.frame, width=80, height=10)
        self.hardware_info_text.pack(pady=10)

    def update_country_list(self):
        countries = ["USA", "Canada", "UK", "Australia", "India", "Germany", "France", "Japan", "China"]
        self.country_combo['values'] = countries
        self.country_combo.current(0)

    def update_language_list(self):
        languages = ["en_US", "en_GB", "fr_FR", "de_DE", "es_ES", "zh_CN", "ja_JP"]
        self.language_combo['values'] = languages
        self.language_combo.current(0)

    def update_locale_list(self):
        locales = ["en_US.UTF-8", "en_GB.UTF-8", "fr_FR.UTF-8", "de_DE.UTF-8", "es_ES.UTF-8", "zh_CN.UTF-8", "ja_JP.UTF-8"]
        self.locale_combo['values'] = locales
        self.locale_combo.current(0)

    def detect_hardware(self):
        try:
            cpu_info = subprocess.check_output("lscpu", shell=True).decode().strip()
            ram_info = subprocess.check_output("free -h", shell=True).decode().strip()
            gpu_info = subprocess.check_output("lspci | grep VGA", shell=True).decode().strip()

            hardware_info = f"CPU:\n{cpu_info}\n\nRAM:\n{ram_info}\n\nGraphics Card:\n{gpu_info}"
            self.hardware_info_text.delete(1.0, tk.END)
            self.hardware_info_text.insert(tk.END, hardware_info)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to detect hardware: {e}")

# Usage example for integration in installer.py:
# user_input_frame = ttk.Frame(notebook)
# notebook.add(user_input_frame, text="User Input")
# user_input.UserInput(user_input_frame)
