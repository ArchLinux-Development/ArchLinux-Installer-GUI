import customtkinter as ctk
from libs.kernel_setup import KernelSetup

class KernelSetupFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.kernel_setup = KernelSetup(self)

    def get_kernel_info(self):
        return {
            "selected_kernel": self.kernel_setup.kernel_var.get()
        }
