import json
import tkinter as tk
from tkinter import ttk
import customtkinter
from app.tcp_client import TCPClient
from .ui.master_gui import MasterGUI
from .components import show_custom_dialog
import uuid
import os
from .config import SERVICE_PORT, SERVICE_HOST

class FolderApp:
    def __init__(self, root):
        self.root = root
        self.setup_gui()
        self.setup_style()
        self.client = TCPClient(SERVICE_HOST, SERVICE_PORT)
        self.home_frame = tk.Frame(root, bg="#ecf0f1")
        self.tags_frame = tk.Frame(root, bg="#ecf0f1")
        self.history_frame = tk.Frame(root, bg="#ecf0f1")
        self.watches = []
        self.show_screen()
        
    def _send_command(self, command, body):
        request = {'command': command, 'body': body}
        request_json = json.dumps(request)
        try:
            self.client.connect()
            self.client.send_message(request_json)
            response = self.client.receive_response()
            print("Received response:", response)
        finally:
            self.client.close_connection()
    
    def _send_command_request(self, command):
        request = {'command': command}
        request_json = json.dumps(request)
        try:
            self.client.connect()
            self.client.send_message(request_json)
            response = self.client.receive_response()
            print("Received response:", response)
        finally:
            self.client.close_connection()
        return json.loads(response)
    
    def setup_gui(self):
        self.root.title("Folder Sorter Menu")
        self.root.geometry("1280x960")
        self.root.option_add("*Font", "helvetica 12")
        self.root.option_add("*TButton*relief", "flat")
        
    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=25, bordercolor="#343638", borderwidth=0)
        style.map('Treeview', background=[('selected', '#22559b')])
        style.configure("Treeview.Heading", relief="flat")
        style.map("Treeview.Heading", background=[('active', '#3484F0')])

    def show_screen(self):
        customtkinter.CTkLabel(self.home_frame, text="Tag Screen", font=("Helvetica", 16)).pack()
        self.tags_frame.pack(fill=tk.BOTH, expand=True)
        self.create_tags_table()
        customtkinter.CTkLabel(self.home_frame, text="History Screen", font=("Helvetica", 16)).pack()
        self.history_frame.pack(fill=tk.BOTH, expand=True)
        self.create_history_table() 

    def create_history_table(self):
        for widget in self.history_frame.winfo_children():
            widget.destroy()
        columns = ("Text", "Create Timestamp")
        tree = ttk.Treeview(self.history_frame, columns=columns, show="headings", selectmode="browse", style="Treeview")
        self.setup_tree(tree, columns)

        logs = self.get_list_logs()
        for log in logs:
            tree.insert("", "end", values=(log.text, log.timestamp))

        tree.pack(padx=10, pady=20, fill=tk.BOTH, expand=True)

    def create_tags_table(self):
        columns = ("Id", "Source Path", "Tags", "Target Path")
        tree = ttk.Treeview(self.tags_frame, columns=columns, show="headings", selectmode="browse", style="Treeview")
        self.setup_tree(tree, columns)

        self.tags = self.get_list_tag_path()
        for row in self.tags:
            tree.insert("", "end", values=(row['id'], row['sourcepath'], row['tags'], row['targetpath']))

        tree.pack(padx=10, pady=20, fill=tk.BOTH, expand=True)
        self.setup_buttons(tree)

    def setup_tree(self, tree, columns):
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=150)

    def setup_buttons(self, tree):
        add_button = customtkinter.CTkButton(self.tags_frame, text="Add", command=lambda: self.add_row(tree))
        add_button.pack(side=tk.LEFT, padx=10)

        remove_button = customtkinter.CTkButton(self.tags_frame, text="Remove", command=lambda: self.remove_row(tree))
        remove_button.pack(side=tk.LEFT, padx=10)

        edit_button = customtkinter.CTkButton(self.tags_frame, text="Edit", command=lambda: self.edit_row(tree))
        edit_button.pack(side=tk.LEFT, padx=10)

        auto_tag = customtkinter.CTkButton(self.tags_frame, text="Auto Tag", command=lambda: self.auto_tag(tree))
        auto_tag.pack(side=tk.LEFT, padx=10)
        
        auto_tag = customtkinter.CTkButton(self.tags_frame, text="Trigger Move", command=lambda: self._trigger_move(tree))
        auto_tag.pack(side=tk.LEFT, padx=10)
        
    def _trigger_move(self, tree):
        selected_item = tree.selection()
        if selected_item:
            current_data = tree.item(selected_item, "values")
            self._send_command('trigger', {'source_path': current_data[1], 'tags': current_data[2], 'target_path': current_data[3]})
            
    def _send_tag_path(self, tag_path, command):
        request_body = {
            "id": str(tag_path['id']),
            "source_path": tag_path['sourcepath'], 
            "tags": tag_path['tags'], 
            "target_path": tag_path['targetpath']
        }
        self._send_command(command, request_body)
            
    def auto_tag(self, tree):
        source_path = show_custom_dialog("Auto Tag", "Enter Source Path:", selectFolder=True)
        if source_path is None:
            return
        target_path = show_custom_dialog("Auto Tag", "Enter Target path for tagging:", selectFolder=True)
        if target_path is None:
            return
        lowest_level_directories = [root for root, dirs, files in os.walk(target_path) if not dirs]
        for path in lowest_level_directories:
            tag = os.path.basename(os.path.normpath(path))
            id = uuid.uuid4()
            self._send_command('add', {
                "id": str(id),
                "source_path": source_path, 
                "tags": tag, 
                "target_path": path
            })
            tree.insert("", "end", values=(id, source_path, tag, path))

    def add_row(self, tree):
        source_path = show_custom_dialog("Add Row", "Enter Source Path:", selectFolder=True)
        if source_path is None:
            return
        tags = show_custom_dialog("Add Row", "Enter Tags:")
        if tags is None:
            return
        target_path = show_custom_dialog("Add Row", "Enter Target Path:", selectFolder=True)
        if target_path is None:
            return
        id = uuid.uuid4()
        self._send_command('add', {
            "id": str(id),
            "source_path": source_path, 
            "tags": tags, 
            "target_path": target_path
        })
        if source_path and tags and target_path:
            tree.insert("", "end", values=(id, source_path, tags, target_path))

    def remove_row(self, tree):
        selected_item = tree.selection()
        current_data = tree.item(selected_item, "values")
        id = current_data[0]
        self._send_command('delete', {
            "id": str(id)
        })
        if selected_item:
            tree.delete(selected_item)

    def edit_row(self, tree):
        selected_item = tree.selection()
        if selected_item:
            current_data = tree.item(selected_item, "values")
            id = current_data[0]
            source_path = show_custom_dialog("Edit Row", "Edit Source Path:", initialvalue=current_data[1], selectFolder=True)
            if source_path is None:
                return
            tags = show_custom_dialog("Edit Row", "Edit Tags:", initialvalue=current_data[2])
            if tags is None:
                return
            target_path = show_custom_dialog("Edit Row", "Edit Target Path:", initialvalue=current_data[3], selectFolder=True)
            if target_path is None:
                return
            if source_path is not None and tags is not None and target_path is not None:
                tree.item(selected_item, values=(current_data[0], source_path, tags, target_path))
            self._send_command('update', {
                "id": str(id),
                "source_path": source_path, 
                "tags": tags, 
                "target_path": target_path
            })
            
    def get_list_tag_path(self):
        return self._send_command_request('list')
    
    def get_list_logs(self):
        return self._send_command_request('logs')
    
if __name__ == "__main__":
    app = MasterGUI()
    app.mainloop()