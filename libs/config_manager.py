import json
import os
from tkinter import filedialog, messagebox

class ConfigManager:
    @staticmethod
    def save_config(config_data, parent_window=None):
        try:
            file_path = filedialog.asksaveasfilename(
                parent=parent_window,
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Save Configuration"
            )
            if not file_path:
                return False

            with open(file_path, 'w') as f:
                json.dump(config_data, f, indent=4)
            
            messagebox.showinfo("Success", f"Configuration saved to {file_path}")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {e}")
            return False

    @staticmethod
    def load_config(parent_window=None):
        try:
            file_path = filedialog.askopenfilename(
                parent=parent_window,
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Load Configuration"
            )
            if not file_path:
                return None

            with open(file_path, 'r') as f:
                config_data = json.load(f)
            
            messagebox.showinfo("Success", f"Configuration loaded from {file_path}")
            return config_data
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load configuration: {e}")
            return None
