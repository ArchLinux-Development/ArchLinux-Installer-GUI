import tkinter as tk
from tkinter import ttk, messagebox
from libs.bootloader import grub, systemd_boot, syslinux, refind, lilo, efistub, clover_efi, elilo

class BootloaderSetup:
    def __init__(self, frame):
        self.frame = frame
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.frame, text="Bootloader Setup:").pack(pady=10)

        self.bootloader_var = tk.StringVar(value="grub")
        bootloaders = ["GRUB", "systemd-boot", "Syslinux", "rEFInd", "LILO", "EFISTUB", "Clover EFI", "Elilo"]

        for bl in bootloaders:
            ttk.Radiobutton(self.frame, text=bl, variable=self.bootloader_var, value=bl.lower()).pack(pady=5)

        self.install_button = ttk.Button(self.frame, text="Install Bootloader", command=self.install_bootloader)
        self.install_button.pack(pady=10)

    def install_bootloader(self):
        bootloader = self.bootloader_var.get()
        if bootloader == "grub":
            message = grub.install_grub()
        elif bootloader == "systemd-boot":
            message = systemd_boot.install_systemd_boot()
        elif bootloader == "syslinux":
            message = syslinux.install_syslinux()
        elif bootloader == "refind":
            message = refind.install_refind()
        elif bootloader == "lilo":
            message = lilo.install_lilo()
        elif bootloader == "efistub":
            message = efistub.install_efistub()
        elif bootloader == "clover efi":
            message = clover_efi.install_clover_efi()
        elif bootloader == "elilo":
            message = elilo.install_elilo()
        else:
            message = "Unknown bootloader selected"

        messagebox.showinfo("Bootloader Installation", message)
