import tkinter as tk
from tkinter import simpledialog
from ttkthemes import ThemedTk

class CustomDialog(simpledialog.Dialog):
    def __init__(self, parent, title, text):
        self.title_text = title
        self.text = text
        super().__init__(parent)

    def body(self, master):
        tk.Label(master, text=self.text, font=("Helvetica", 12)).grid(row=0, pady=10)

        self.entry = tk.Entry(master, font=("Helvetica", 12))
        self.entry.grid(row=1, column=0, columnspan=2, pady=10, padx=10, ipadx=10, ipady=5, sticky="ew")

        return self.entry

    def apply(self):
        result = self.entry.get()
        self.result = result

def show_custom_dialog(title, text):
    root = ThemedTk(theme="arc")  
    root.withdraw()

    dialog = CustomDialog(root, title, text)
    result = dialog.result

    root.destroy()

    return result
