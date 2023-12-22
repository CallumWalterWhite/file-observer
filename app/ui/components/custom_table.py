import tkinter as tk
from tkinter import ttk

class CustomTable(tk.Frame):
    def __init__(self, parent, columns):
        super().__init__(parent)
        self.columns = columns
        self.data = []
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        self.setup_tree()
        self.tree.pack(fill="both", expand=True)

    def setup_tree(self):
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)

    def add_row(self, values):
        self.tree.insert("", "end", values=values)
        self.data.append(values)

    def edit_row(self, row_id, values):
        selected_item = self.tree.selection()
        if selected_item:
            index = self.tree.index(selected_item)
            self.tree.item(selected_item, values=values)
            self.data[index] = values

    def remove_row(self, row_id):
        selected_item = self.tree.selection()
        if selected_item:
            index = self.tree.index(selected_item)
            self.tree.delete(selected_item)
            del self.data[index]

    def clear_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.data = []