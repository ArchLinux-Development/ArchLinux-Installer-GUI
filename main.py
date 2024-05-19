import tkinter as tk
from tkinter import messagebox
from utils import show_splash_screen
from arch_installer import ArchInstaller
from libs.environment import is_virtual_environment, is_arch_linux  # Import the functions

def start_main_app(root):
    print("Starting main application")  # Debugging statement
    root.destroy()  # Destroy the root window used for the splash screen
    app = ArchInstaller()
    app.mainloop()

if __name__ == "__main__":
    print("Starting main.py")  # Debugging statement
    root = tk.Tk()
    root.withdraw()  # Hide the main window while showing the splash screen

    # Check if running on Arch Linux
    if not is_arch_linux():
        print("Not running on Arch Linux")  # Debugging statement
        messagebox.showerror("OS Check", "This installer only supports Arch Linux.")
        root.destroy()
        exit(1)

    # Show splash screen and schedule its destruction
    splash = tk.Toplevel(root)
    splash.geometry("400x300")
    splash.overrideredirect(True)
    splash.configure(bg='white')
    label = tk.Label(splash, text="Splash Screen", font=("Helvetica", 24), bg='white')
    label.pack(expand=True)

    def close_splash_and_start_app():
        splash.destroy()
        start_main_app(root)

    root.after(3000, close_splash_and_start_app)  # Show splash screen for 3 seconds
    root.mainloop()
