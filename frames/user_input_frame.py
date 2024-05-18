import tkinter as tk
from tkinter import ttk
from libs.user_input import UserInput

class UserInputFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.user_input = UserInput(self)

    def get_user_info(self):
        return self.user_input.get_user_info()
