import tkinter as tk
from tkinter import ttk
import customtkinter

class LogsGUI(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.setup_style()
        customtkinter.CTkLabel(self, text="Logs Screen", font=("Helvetica", 16)).pack()
        self.create_logs_table()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=25, bordercolor="#343638", borderwidth=0)
        style.map('Treeview', background=[('selected', '#22559b')])
        style.configure("Treeview.Heading", relief="flat")
        style.map("Treeview.Heading", background=[('active', '#3484F0')])
    
    def create_logs_table(self):
        for widget in self.winfo_children():
            widget.destroy()
        columns = ("Text", "Create Timestamp")
        tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse", style="Treeview")
        self.setup_tree(tree, columns)

        logs = self.master.folder_service_adapter.get_list_logs()
        for log in logs:
            tree.insert("", "end", values=(log.text, log.timestamp))

        tree.pack(padx=10, pady=20, fill=tk.BOTH, expand=True)

    def setup_tree(self, tree, columns):
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=150)