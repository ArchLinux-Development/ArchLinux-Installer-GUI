import tkinter as tk
from tkinter import ttk, messagebox
from frames import IntroFrame, UserInputFrame, NetworkSetupFrame, KernelSetupFrame, FilesystemSetupFrame, BootloaderSetupFrame, SwapSetupFrame, DesktopEnvironmentFrame, PackagesSetupFrame, ConfirmationFrame
from utils import show_splash_screen
from libs.intro import get_intro_text  # Import the intro text function
from libs.final_arch_installer import create_filesystem, run_chaotic_aur_setup, run_cachyos_repo_setup, run_command

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
        self.display_intro(intro_frame)

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
        self.perform_installation()

        messagebox.showinfo("Installation", "Installation process started. Check the console for details.")

    def perform_installation(self):
        fs_info = self.filesystem_setup.get_filesystem_info()
        if not fs_info["device"]:
            messagebox.showerror("Error", "No device selected for filesystem.")
            return

        create_filesystem(fs_info["filesystem"], fs_info["device"])
        run_chaotic_aur_setup()
        run_cachyos_repo_setup()
        # Add more steps as needed, calling functions from final_arch_installer

    def display_intro(self, parent):
        """Display the introduction to the script."""
        intro_text = get_intro_text()
        intro_label = tk.Label(parent, text=intro_text, justify=tk.CENTER)
        intro_label.pack(expand=True, padx=10, pady=10)

if __name__ == "__main__":
    app = ArchInstaller()
    app.mainloop()
