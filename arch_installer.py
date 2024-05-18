import tkinter as tk
from tkinter import ttk, messagebox
from frames.intro_frame import IntroFrame
from frames.user_input_frame import UserInputFrame
from frames.network_setup_frame import NetworkSetupFrame
from frames.kernel_setup_frame import KernelSetupFrame
from frames.filesystem_setup_frame import FilesystemSetupFrame
from frames.bootloader_setup_frame import BootloaderSetupFrame
from frames.swap_setup_frame import SwapSetupFrame
from frames.desktop_environment_frame import DesktopEnvironmentFrame
from frames.packages_setup_frame import PackagesSetupFrame
from frames.confirmation_frame import ConfirmationFrame
from utils import show_splash_screen

class ArchInstaller(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Arch Linux Installer")
        self.geometry("1020x600")
        self.packages_setup = None  # To be set later
        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self)

        intro_frame = IntroFrame(notebook)
        notebook.add(intro_frame, text="Introduction")

        user_input_frame = UserInputFrame(notebook)
        notebook.add(user_input_frame, text="User Input")
        self.user_input = user_input_frame

        network_frame = NetworkSetupFrame(notebook)
        notebook.add(network_frame, text="Network Setup")
        self.network_setup = network_frame

        kernel_frame = KernelSetupFrame(notebook)
        notebook.add(kernel_frame, text="Kernel Setup")

        filesystem_frame = FilesystemSetupFrame(notebook)
        notebook.add(filesystem_frame, text="Filesystem Setup")

        bootloader_frame = BootloaderSetupFrame(notebook)
        notebook.add(bootloader_frame, text="Bootloader Setup")

        swap_frame = SwapSetupFrame(notebook)
        notebook.add(swap_frame, text="Swap Setup")

        desktop_environment_frame = DesktopEnvironmentFrame(notebook, tk.StringVar())
        notebook.add(desktop_environment_frame, text="Desktop Environment Setup")
        self.desktop_environment_setup = desktop_environment_frame

        packages_frame = PackagesSetupFrame(notebook, self.desktop_environment_setup.desktop_env_var)
        notebook.add(packages_frame, text="Packages Setup")
        self.packages_setup = packages_frame

        confirm_frame = ConfirmationFrame(notebook, self)
        notebook.add(confirm_frame, text="Confirmation")
        self.confirm_frame = confirm_frame

        notebook.pack(expand=True, fill="both")
        notebook.bind("<<NotebookTabChanged>>", self.refresh_summary)

    def refresh_summary(self, event):
        self.confirm_frame.update_summary(
            user_info=self.user_input.get_user_info(),
            network_info=self.network_setup.get_network_info(),
            kernel_info="Kernel settings to be added here.",  # Replace with actual kernel settings
            filesystem_info="Filesystem settings to be added here.",  # Replace with actual filesystem settings
            bootloader_info="Bootloader settings to be added here.",  # Replace with actual bootloader settings
            swap_info="Swap settings to be added here.",  # Replace with actual swap settings
            desktop_env_info=self.desktop_environment_setup.get_desktop_env_info(),
            packages_info="Packages settings to be added here."  # Replace with actual packages settings
        )

    def start_installation(self):
        if not self.desktop_environment_setup.validate_selection():
            return

        user_info = self.user_input.get_user_info()

        if self.packages_setup.chaotic_aur_var.get():
            self.packages_setup.setup_chaotic_aur()

        if self.packages_setup.cachyos_repo_var.get():
            self.packages_setup.setup_cachyos_repo()

        print("Starting installation...")
        print(f"User Info: {user_info}")
        # Add other installation steps here
        # e.g., partitioning, mounting filesystems, pacstrap, etc.
        messagebox.showinfo("Installation", "Installation process started. Check the console for details.")
