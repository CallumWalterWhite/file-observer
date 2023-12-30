import tkinter as tk
import tkinter.messagebox
import customtkinter
from app.folder_service_adapter import FolderServiceAdapter
from .rules_view_gui import RuleViewGUI
from .home_gui import HomeGUI
from .logs_gui import LogsGUI

# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("System")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("dark-blue")

class MasterGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.folder_service_adapter = FolderServiceAdapter()
        # configure window
        self.title("File Observer")
        self.geometry("1280x960")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)  # Expand the second column

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(
            self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="File Observer", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        # create sidebar buttons
        routes = [
            ("Home", self.show_home),
            ("Rules", self.show_rules),
            ("Logs", self.show_logs)
        ]
        for route in routes:
            button = customtkinter.CTkButton(
                self.sidebar_frame, text=route[0], command=route[1])
            button.grid(row=routes.index(route)+1, column=0, padx=20, pady=10)
        self.main_frame = None
        self.main_frame_header = None
        self.show_home()

    def show_home(self):
        if self.main_frame_header == "Home":
            return
        if self.main_frame is not None:
            self.main_frame.destroy()
        self.main_frame = HomeGUI(self)
        self.main_frame_header = "Home"

    def show_rules(self):
        if self.main_frame_header == "Rules":
            return
        if self.main_frame is not None:
            self.main_frame.destroy()
        self.main_frame = RuleViewGUI(self)
        self.main_frame_header = "Rules"

    def show_logs(self):
        if self.main_frame_header == "Logs":
            return
        if self.main_frame is not None:
            self.main_frame.destroy()
        self.main_frame = LogsGUI(self)
        self.main_frame_header = "Logs"
