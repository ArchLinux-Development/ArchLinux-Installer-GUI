import tkinter as tk
from tkinter import ttk, messagebox
from . import gnome, kde_plasma, xfce, lxde, lxqt, cinnamon, mate, budgie, deepin, enlightenment

class DesktopEnvironmentSetup:
    def __init__(self, frame):
        self.frame = frame
        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.frame, text="Desktop Environment Setup:").pack(pady=10)

        self.de_var = tk.StringVar(value="gnome")
        environments = ["GNOME", "KDE Plasma", "Xfce", "LXDE", "LXQt", "Cinnamon", "MATE", "Budgie", "Deepin", "Enlightenment"]

        for de in environments:
            ttk.Radiobutton(self.frame, text=de, variable=self.de_var, value=de.lower().replace(' ', '_')).pack(pady=5)

        self.install_button = ttk.Button(self.frame, text="Install Desktop Environment", command=self.install_de)
        self.install_button.pack(pady=10)

    def install_de(self):
        de = self.de_var.get()
        if de == "gnome":
            message = gnome.install_gnome()
        elif de == "kde_plasma":
            message = kde_plasma.install_kde_plasma()
        elif de == "xfce":
            message = xfce.install_xfce()
        elif de == "lxde":
            message = lxde.install_lxde()
        elif de == "lxqt":
            message = lxqt.install_lxqt()
        elif de == "cinnamon":
            message = cinnamon.install_cinnamon()
        elif de == "mate":
            message = mate.install_mate()
        elif de == "budgie":
            message = budgie.install_budgie()
        elif de == "deepin":
            message = deepin.install_deepin()
        elif de == "enlightenment":
            message = enlightenment.install_enlightenment()
        else:
            message = "Unknown desktop environment selected"

        messagebox.showinfo("Desktop Environment Installation", message)
