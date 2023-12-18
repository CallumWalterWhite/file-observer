from tkinter import *
import customtkinter
from app.folder_app import FolderApp

if __name__ == "__main__":
    root = customtkinter.CTk()
    app = FolderApp(root)
    root.mainloop()
    