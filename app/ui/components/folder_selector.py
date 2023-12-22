import tkinter as tk
from tkinter import filedialog

class FolderSelector(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.select_button = tk.Button(self, text="Select Folder", command=self.ask_directory)
        self.select_button.pack(pady=10)

        self.selected_directory = tk.StringVar()

        self.directory_entry = tk.Entry(self, textvariable=self.selected_directory, state='disabled', width=40)
        self.directory_entry.pack(pady=10)

        self.show_contents_button = tk.Button(self, text="Show Contents", command=self.show_folder_contents)
        self.show_contents_button.pack(pady=10)

        self.contents_text = tk.Text(self, height=5, width=40, state='disabled')
        self.contents_text.pack(pady=10)

    def ask_directory(self):
        selected_folder = filedialog.askdirectory()
        self.selected_directory.set(selected_folder)

    def show_folder_contents(self):
        folder_path = self.selected_directory.get()
        if folder_path:
            try:
                with open(f"{folder_path}/folder_contents.txt", 'r') as file:
                    contents = file.read()
                    self.contents_text.config(state='normal')
                    self.contents_text.delete('1.0', tk.END)
                    self.contents_text.insert(tk.END, contents)
                    self.contents_text.config(state='disabled')
            except FileNotFoundError:
                self.contents_text.config(state='normal')
                self.contents_text.delete('1.0', tk.END)
                self.contents_text.insert(tk.END, "File not found.")
                self.contents_text.config(state='disabled')