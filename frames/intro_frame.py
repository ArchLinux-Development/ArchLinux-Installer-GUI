import tkinter as tk
from tkinter import ttk

class IntroFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_intro()

    def create_intro(self):
        intro_label = ttk.Label(self, text="Welcome to the Arch Linux Installer!\n\nThis installer will guide you through the process of setting up Arch Linux on your system.\n\nClick on the tabs above to configure each part of the installation process.", wraplength=600, justify="center")
        intro_label.pack(expand=True, fill="both")
