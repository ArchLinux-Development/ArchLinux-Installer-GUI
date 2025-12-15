import customtkinter as ctk
from libs.user_input import UserInput

class UserInputFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.user_input = UserInput(self)

    def get_user_info(self):
        return self.user_input.get_user_info()
