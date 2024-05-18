import tkinter as tk
from tkinter import messagebox
from utils import show_splash_screen
from arch_installer import ArchInstaller
from libs.environment import is_virtual_environment, is_arch_linux  # Import the functions

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main window while showing the splash screen

    # Check if running on Arch Linux
    if not is_arch_linux():
        messagebox.showerror("OS Check", "This installer only supports Arch Linux.")
        root.destroy()
        exit(1)

    # Show splash screen and schedule its destruction
    show_splash_screen(root, "splash.png", duration=3000)

    def start_main_app():
        root.deiconify()
        
        # Check if running in a virtual environment
        if is_virtual_environment():
            tk.messagebox.showinfo("Environment Check", "Running in a virtual environment")
        else:
            tk.messagebox.showinfo("Environment Check", "Running on physical hardware")
        
        app = ArchInstaller()
        app.mainloop()

    # Wait for the splash screen to finish before showing the main window
    root.after(3000, start_main_app)

    root.mainloop()
