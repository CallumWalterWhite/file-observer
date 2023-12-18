from tkinter import *
import customtkinter
from app.main import FolderApp
from service.main import main

if __name__ == "__main__":
    main()
    root = customtkinter.CTk()
    app = FolderApp(root)
    root.mainloop()
    