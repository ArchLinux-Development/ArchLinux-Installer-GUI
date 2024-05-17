import tkinter as tk
from tkinter import ttk
from libs import user_input, network, filesystem, swap
from libs.bootloader.bootloader_setup import BootloaderSetup
from libs.desktop_environment.desktop_environment_setup import DesktopEnvironmentSetup

class ArchInstaller(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Arch Linux Installer")
        self.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self)

        intro_frame = ttk.Frame(notebook)
        notebook.add(intro_frame, text="Introduction")
        self.create_intro(intro_frame)

        user_input_frame = ttk.Frame(notebook)
        notebook.add(user_input_frame, text="User Input")
        user_input.UserInput(user_input_frame)

        network_frame = ttk.Frame(notebook)
        notebook.add(network_frame, text="Network Setup")
        network.NetworkSetup(network_frame)

        filesystem_frame = ttk.Frame(notebook)
        notebook.add(filesystem_frame, text="Filesystem Setup")
        filesystem.FilesystemSetup(filesystem_frame)

        bootloader_frame = ttk.Frame(notebook)
        notebook.add(bootloader_frame, text="Bootloader Setup")
        BootloaderSetup(bootloader_frame)

        swap_frame = ttk.Frame(notebook)
        notebook.add(swap_frame, text="Swap Setup")
        swap.SwapSetup(swap_frame)

        desktop_environment_frame = ttk.Frame(notebook)
        notebook.add(desktop_environment_frame, text="Desktop Environment Setup")
        DesktopEnvironmentSetup(desktop_environment_frame)

        confirm_frame = ttk.Frame(notebook)
        notebook.add(confirm_frame, text="Confirmation")
        self.create_confirmation(confirm_frame)

        notebook.pack(expand=True, fill="both")

    def create_intro(self, frame):
        intro_label = ttk.Label(frame, text="Welcome to the Arch Linux Installer!\n\nThis installer will guide you through the process of setting up Arch Linux on your system.\n\nClick on the tabs above to configure each part of the installation process.", wraplength=600, justify="center")
        intro_label.pack(expand=True, fill="both")

    def create_confirmation(self, frame):
        confirm_label = ttk.Label(frame, text="Review all your settings before proceeding with the installation.", wraplength=600, justify="center")
        confirm_label.pack(pady=10)
        
        confirm_button = ttk.Button(frame, text="Proceed with Installation", command=self.start_installation)
        confirm_button.pack(pady=10)

    def start_installation(self):
        print("Starting installation...")

if __name__ == "__main__":
    app = ArchInstaller()
    app.mainloop()
