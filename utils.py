import tkinter as tk
from tkinter import ttk

def show_splash_screen(root, image_path, duration):
    splash = tk.Toplevel(root)
    splash.geometry("300x200")
    splash.title("Splash Screen")
    label = ttk.Label(splash, text="Splash Screen", image=tk.PhotoImage(file=image_path))
    label.pack(expand=True, fill="both")
    root.after(duration, splash.destroy)
