import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import sys
import threading
from frames import (IntroFrame, UserInputFrame, NetworkSetupFrame, KernelSetupFrame, 
                    FilesystemSetupFrame, BootloaderSetupFrame, SwapSetupFrame, 
                    DesktopEnvironmentFrame, PackagesSetupFrame, ConfirmationFrame,
                    InstallationProgressFrame)
from utils import show_splash_screen
from libs.intro import get_intro_text
from libs.final_arch_installer import (create_filesystem, run_chaotic_aur_setup, 
                                       run_cachyos_repo_setup, install_microcode, run_command)

ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class ArchInstaller(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Arch Linux Installer")
        self.geometry("1020x700")
        
        # Configure grid layout (1x1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.current_frame_index = 0
        self.frame_order = []

        self.create_widgets()
        self.show_frame(self.frame_order[0])

    def create_widgets(self):
        # Main container for frames
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True, padx=10, pady=10)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Initialize frames
        self.initialize_frames()

        # Navigation Buttons
        self.button_frame = ctk.CTkFrame(self, height=50)
        self.button_frame.pack(fill="x", padx=10, pady=10)

        self.back_button = ctk.CTkButton(self.button_frame, text="Back", command=self.go_back, state="disabled")
        self.back_button.pack(side="left", padx=10)

        self.next_button = ctk.CTkButton(self.button_frame, text="Next", command=self.go_next)
        self.next_button.pack(side="right", padx=10)

    def initialize_frames(self):
        # Define the order of frames for the wizard
        frame_classes = [
            IntroFrame,
            UserInputFrame,
            NetworkSetupFrame,
            KernelSetupFrame,
            FilesystemSetupFrame,
            BootloaderSetupFrame,
            SwapSetupFrame,
            DesktopEnvironmentFrame,
            PackagesSetupFrame,
            ConfirmationFrame,
            InstallationProgressFrame
        ]
        
        # We need to pass shared variables or references if needed
        # For now, instantiating them with self.container as parent
        # Note: frames need to be adapted to accept container and be ctk frames
        
        # Shared variables (moved from original code)
        self.desktop_env_var = tk.StringVar()

        for F in frame_classes:
            if F == DesktopEnvironmentFrame:
                frame = F(self.container, self.desktop_env_var)
            elif F == PackagesSetupFrame:
                frame = F(self.container, self.desktop_env_var)
            elif F == ConfirmationFrame:
                frame = F(self.container, self) # Confirm frame needs 'controller' (self)
            elif F == InstallationProgressFrame:
                frame = F(self.container)
            else:
                frame = F(self.container)

            self.frames[F.__name__] = frame
            try:
               frame.grid(row=0, column=0, sticky="nsew")
            except Exception as e:
                print(f"Error packing {F.__name__}: {e}")

        # Store the order by name for easy navigation
        self.frame_order = [F.__name__ for F in frame_classes]
        
        # Save references for get_user_info style access
        self.user_input = self.frames["UserInputFrame"]
        self.network_setup = self.frames["NetworkSetupFrame"]
        self.kernel_setup = self.frames["KernelSetupFrame"]
        self.filesystem_setup = self.frames["FilesystemSetupFrame"]
        self.swap_setup = self.frames["SwapSetupFrame"]
        self.desktop_environment_setup = self.frames["DesktopEnvironmentFrame"]
        self.packages_setup = self.frames["PackagesSetupFrame"]
        self.confirm_frame = self.frames["ConfirmationFrame"]
        self.installation_progress = self.frames["InstallationProgressFrame"]

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()
        
        # Update Intro text if it's the intro frame (special case from original code)
        if frame_name == "IntroFrame":
             self.display_intro(frame)

        # Update Summary if it's confirmation frame
        if frame_name == "ConfirmationFrame":
             self.refresh_summary()

    def go_next(self):
        if self.current_frame_index < len(self.frame_order) - 1:
            # Add validation hooks here if necessary
            # e.g. if not self.frames[self.frame_order[self.current_frame_index]].validate(): return

            self.current_frame_index += 1
            self.update_navigation_buttons()
            self.show_frame(self.frame_order[self.current_frame_index])

    def go_back(self):
        if self.current_frame_index > 0:
            self.current_frame_index -= 1
            self.update_navigation_buttons()
            self.show_frame(self.frame_order[self.current_frame_index])

    def update_navigation_buttons(self):
        # Back button
        if self.current_frame_index == 0 or self.frame_order[self.current_frame_index] == "InstallationProgressFrame":
            self.back_button.configure(state="disabled")
        else:
            self.back_button.configure(state="normal")
            
        # Next button / Install button
        if self.current_frame_index == len(self.frame_order) - 2: # Confirmation Frame is second to last now
            self.next_button.configure(text="Install", state="normal", command=self.start_installation)
        elif self.frame_order[self.current_frame_index] == "InstallationProgressFrame":
             self.next_button.configure(text="Finish", state="disabled", command=self.destroy) 
        else:
            self.next_button.configure(text="Next", state="normal", command=self.go_next)

    def refresh_summary(self, event=None):
        # Update summary if the confirmation frame is visible or about to be shown
        if hasattr(self, 'confirm_frame'):
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

        # Move to progress frame
        self.current_frame_index += 1
        self.update_navigation_buttons()
        self.show_frame(self.frame_order[self.current_frame_index])

        # Start installation in a separate thread
        threading.Thread(target=self.run_installation_thread, daemon=True).start()

    def run_installation_thread(self):
        # Redirect stdout/stderr
        class OutputRedirector:
            def __init__(self, text_widget, app):
                self.text_widget = text_widget
                self.app = app

            def write(self, string):
                # Schedule update on main thread
                self.app.after(0, lambda: self.text_widget.append_text(string))

            def flush(self):
                pass
        
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        
        sys.stdout = OutputRedirector(self.installation_progress, self)
        sys.stderr = OutputRedirector(self.installation_progress, self)

        try:
            print("Starting installation...")
            print(f"Configuration: {install_config}")
            self.perform_installation(install_config)
            print("Installation Complete!")
            self.after(0, lambda: self.next_button.configure(state="normal")) # Enable Finish button
        except Exception as e:
            print(f"Installation failed: {e}")
            import traceback
            traceback.print_exc()
        finally:
            sys.stdout = original_stdout
            sys.stderr = original_stderr

    def perform_installation(self, config):
        fs_info = config["filesystem_info"]
        if not fs_info["device"]:
            print("Error: No device selected for filesystem.") # Print to console widget
            return

        create_filesystem(fs_info["filesystem"], fs_info["device"])
        run_chaotic_aur_setup()
        run_cachyos_repo_setup()
        install_microcode()
        # Add more steps as needed, calling functions from final_arch_installer

    def display_intro(self, parent):
        intro_text = get_intro_text()
        intro_label = ctk.CTkLabel(parent, text=intro_text, justify="center")
        intro_label.pack(expand=True, padx=10, pady=10)

if __name__ == "__main__":
    app = ArchInstaller()
    app.mainloop()
