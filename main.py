import tkinter as tk
from utils import show_splash_screen
from arch_installer import ArchInstaller

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main window while showing the splash screen

    # Show splash screen and schedule its destruction
    show_splash_screen(root, "splash.png", duration=3000)

    def start_main_app():
        root.deiconify()
        app = ArchInstaller()
        app.mainloop()

    # Wait for the splash screen to finish before showing the main window
    root.after(3000, start_main_app)

    root.mainloop()
