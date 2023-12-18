import tkinter as tk
import customtkinter
from tkinter import simpledialog
from tkinter import filedialog

class CustomDialog(simpledialog.Dialog):
    def __init__(self, parent, title, text, initialvalue=None, selectFolder=False):
        self.title_text = title
        self.text = text
        self.initialvalue = initialvalue
        self.selectFolder = selectFolder
        super().__init__(parent)

    def body(self, master):
        customtkinter.CTkLabel(master, text=self.text, font=("Helvetica", 12)).grid(row=0, pady=10)

        self.entry = customtkinter.CTkEntry(master, font=("Helvetica", 12))
        self.entry.grid(row=1, column=0, columnspan=2, pady=10, padx=10, ipadx=10, ipady=5, sticky="ew")

        if self.initialvalue is not None:
            self.entry.insert(0, self.initialvalue)
        
        if self.selectFolder is True:
            def askdir():
              selectedFolder = filedialog.askdirectory()
              self.entry.delete(0, tk.END)
              self.entry.insert(0, selectedFolder)
            self.select_button = customtkinter.CTkButton(self, text="Select Folder", command=askdir)
            self.select_button.pack()
        
        return self.entry

    def apply(self):
        result = self.entry.get()
        self.result = result