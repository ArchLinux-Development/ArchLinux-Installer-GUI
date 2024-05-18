import tkinter as tk
from utils import show_splash_screen
from arch_installer import ArchInstaller
from libs.environment import is_virtual_environment  # Ensure the correct import

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main window while showing the splash screen

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
