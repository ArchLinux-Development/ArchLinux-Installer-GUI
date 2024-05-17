import tkinter as tk
from PIL import Image, ImageTk

class SplashScreen(tk.Toplevel):
    def __init__(self, parent, image_path):
        super().__init__(parent)
        self.image_path = image_path
        self.setup_ui()

    def setup_ui(self):
        self.geometry("600x400")
        self.overrideredirect(True)  # Remove window decorations

        img = Image.open(self.image_path)
        self.img = ImageTk.PhotoImage(img)
        self.img_label = tk.Label(self, image=self.img)
        self.img_label.pack()

def show_splash_screen(root, image_path, duration=3000):
    splash = SplashScreen(root, image_path)
    root.after(duration, splash.destroy)
