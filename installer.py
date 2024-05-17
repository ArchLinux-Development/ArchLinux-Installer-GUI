import tkinter as tk
from tkinter import ttk, messagebox
from libs import UserInput, NetworkSetup, SwapSetup, show_splash_screen, FilesystemSetup, BootloaderSetup, DesktopEnvironmentSetup, PackagesSetup, KernelSetup

class ArchInstaller(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Arch Linux Installer")
        self.geometry("1020x600")
        self.packages_setup = None  # To be set later
        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self)

        intro_frame = ttk.Frame(notebook)
        notebook.add(intro_frame, text="Introduction")
        self.create_intro(intro_frame)

        user_input_frame = ttk.Frame(notebook)
        notebook.add(user_input_frame, text="User Input")
        self.user_input = UserInput(user_input_frame)

        network_frame = ttk.Frame(notebook)
        notebook.add(network_frame, text="Network Setup")
        NetworkSetup(network_frame)

        kernel_frame = ttk.Frame(notebook)
        notebook.add(kernel_frame, text="Kernel Setup")
        KernelSetup(kernel_frame)

        filesystem_frame = ttk.Frame(notebook)
        notebook.add(filesystem_frame, text="Filesystem Setup")
        FilesystemSetup(filesystem_frame)

        bootloader_frame = ttk.Frame(notebook)
        notebook.add(bootloader_frame, text="Bootloader Setup")
        BootloaderSetup(bootloader_frame)

        swap_frame = ttk.Frame(notebook)
        notebook.add(swap_frame, text="Swap Setup")
        SwapSetup(swap_frame)

        desktop_environment_frame = ttk.Frame(notebook)
        notebook.add(desktop_environment_frame, text="Desktop Environment Setup")
        self.desktop_environment_setup = DesktopEnvironmentSetup(desktop_environment_frame, tk.StringVar())

        packages_frame = ttk.Frame(notebook)
        notebook.add(packages_frame, text="Packages Setup")
        self.packages_setup = PackagesSetup(packages_frame, self.desktop_environment_setup.desktop_env_var)

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
        
        confirm_button = ttk.Button(frame, text="Start Installation", command=self.start_installation)
        confirm_button.pack(pady=10)

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
