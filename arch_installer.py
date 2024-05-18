import tkinter as tk
from tkinter import ttk, messagebox
from frames import IntroFrame, UserInputFrame, NetworkSetupFrame, KernelSetupFrame, FilesystemSetupFrame, BootloaderSetupFrame, SwapSetupFrame, DesktopEnvironmentFrame, PackagesSetupFrame, ConfirmationFrame
from utils import show_splash_screen
import subprocess

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
        self.kernel_setup = kernel_frame

        filesystem_frame = FilesystemSetupFrame(notebook)
        notebook.add(filesystem_frame, text="Filesystem Setup")
        self.filesystem_setup = filesystem_frame

        bootloader_frame = BootloaderSetupFrame(notebook)
        notebook.add(bootloader_frame, text="Bootloader Setup")

        swap_frame = SwapSetupFrame(notebook)
        notebook.add(swap_frame, text="Swap Setup")
        self.swap_setup = swap_frame

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
            kernel_info=self.kernel_setup.get_kernel_info(),
            filesystem_info=self.filesystem_setup.get_filesystem_info(),
            bootloader_info="Bootloader settings to be added here.",  # Replace with actual bootloader settings
            swap_info=self.swap_setup.get_swap_info(),
            desktop_env_info=self.desktop_environment_setup.get_desktop_env_info(),
            packages_info=self.packages_setup.get_packages_info()
        )

    def start_installation(self):
        if not self.desktop_environment_setup.validate_selection():
            return

        user_info = self.user_input.get_user_info()

        print("Starting installation...")
        print(f"User Info: {user_info}")

        # Defer filesystem creation to the end
        self.create_filesystem()

        # Add other installation steps here
        # e.g., partitioning, mounting filesystems, pacstrap, etc.
        messagebox.showinfo("Installation", "Installation process started. Check the console for details.")

    def create_filesystem(self):
        fs_info = self.filesystem_setup.get_filesystem_info()
        if not fs_info["device"]:
            messagebox.showerror("Error", "No device selected for filesystem.")
            return

        fs_type = fs_info["filesystem"]
        device = fs_info["device"]

        try:
            if fs_type == "ext4":
                subprocess.run(['mkfs.ext4', device], check=True)
            elif fs_type == "btrfs":
                subprocess.run(['mkfs.btrfs', device], check=True)
            elif fs_type == "zfs":
                subprocess.run(['zpool create mypool', device], check=True)
            elif fs_type == "xfs":
                subprocess.run(['mkfs.xfs', device], check=True)
            elif fs_type == "jfs":
                subprocess.run(['mkfs.jfs', device], check=True)
            elif fs_type == "reiserfs":
                subprocess.run(['mkfs.reiserfs', device], check=True)
            elif fs_type == "f2fs":
                subprocess.run(['mkfs.f2fs', device], check=True)
            else:
                messagebox.showerror("Error", f"Unknown filesystem type: {fs_type}")
                return

            messagebox.showinfo("Filesystem Creation", f"Filesystem {fs_type} created successfully on {device}.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Filesystem Creation Error", f"Failed to create filesystem: {e}")
