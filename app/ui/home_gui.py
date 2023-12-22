import tkinter as tk
import customtkinter

class HomeGUI(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.textbox = customtkinter.CTkTextbox(self, width=400, corner_radius=0)
        self.textbox.grid(row=0, column=0, sticky="nsew")
        self.textbox.insert("0.0", "FileSorter is a Python application designed to automate the tagging and organization of files in directories. It allows users to define rules for tagging files based on specific criteria and then move them to designated target directories.!\n")