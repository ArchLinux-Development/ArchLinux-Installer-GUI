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
        self.network_setup = NetworkSetup(network_frame)

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

        notebook.bind("<<NotebookTabChanged>>", self.refresh_summary)

    def create_intro(self, frame):
        intro_label = ttk.Label(frame, text="Welcome to the Arch Linux Installer!\n\nThis installer will guide you through the process of setting up Arch Linux on your system.\n\nClick on the tabs above to configure each part of the installation process.", wraplength=600, justify="center")
        intro_label.pack(expand=True, fill="both")

    def create_confirmation(self, frame):
        self.confirm_label = ttk.Label(frame, text="Review all your settings before proceeding with the installation.", wraplength=600, justify="center")
        self.confirm_label.pack(pady=10)
        
        self.summary_text = tk.Text(frame, height=20, width=100, wrap="word")
        self.summary_text.pack(pady=10)

        confirm_button = ttk.Button(frame, text="Start Installation", command=self.start_installation)
        confirm_button.pack(pady=10)

    def refresh_summary(self, event):
        self.summary_text.delete(1.0, tk.END)

        user_info = self.user_input.get_user_info()
        network_info = f"Network Interface: {self.network_setup.network_var.get()}\nWiFi SSID: {self.network_setup.wifi_ssid_var.get()}\nConnection Status: {self.network_setup.connection_status_var.get()}"
        kernel_info = "Kernel settings to be added here."  # Replace with actual kernel settings
        filesystem_info = "Filesystem settings to be added here."  # Replace with actual filesystem settings
        bootloader_info = "Bootloader settings to be added here."  # Replace with actual bootloader settings
        swap_info = "Swap settings to be added here."  # Replace with actual swap settings
        desktop_env_info = f"Desktop Environment: {self.desktop_environment_setup.desktop_env_var.get()}\nXorg: {self.desktop_environment_setup.xorg_var.get()}\nWayland: {self.desktop_environment_setup.wayland_var.get()}"
        packages_info = "Packages settings to be added here."  # Replace with actual packages settings

        summary = (
            f"User Information:\n"
            f"Username: {user_info['username']}\n"
            f"Admin Rights: {user_info['admin_rights']}\n"
            f"Country: {user_info['country']}\n"
            f"Language: {user_info['language']}\n\n"
            f"Network Information:\n{network_info}\n\n"
            f"{kernel_info}\n\n"
            f"{filesystem_info}\n\n"
            f"{bootloader_info}\n\n"
            f"{swap_info}\n\n"
            f"{desktop_env_info}\n\n"
            f"{packages_info}"
        )

        self.summary_text.insert(tk.END, summary)

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
