import tkinter as tk
import tkinter.messagebox
import customtkinter
from .rules_view_gui import RuleViewGUI
from .home_gui import HomeGUI

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class MasterGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("File Observer")
        self.geometry("1280x960")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)  # Expand the second column

         # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="File Observer", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Home", command=self.show_home)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Rules", command=self.show_rules)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Logs", command=self.show_logs)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.main_frame=None
        self.show_home()
        
    def show_home(self):
        if self.main_frame is not None:
            self.main_frame.destroy()
        self.main_frame=HomeGUI(self)
        
    def show_rules(self):
        if self.main_frame is not None:
            self.main_frame.destroy()
        self.main_frame=RuleViewGUI(self)
        
    def show_logs(self):
        if self.main_frame is not None:
            self.main_frame.destroy()
        self.main_frame=RuleViewGUI(self)
