import json
import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import uuid
import customtkinter
from .components import show_custom_dialog, get_plus_icon, FolderSelector
from app.folder_service_adapter import FolderServiceAdapter

class RuleViewSingleWindowGUI(customtkinter.CTkToplevel):
    def __init__(self, parent, tree, item_id = None):
        super().__init__(parent)
        self.adapter = FolderServiceAdapter()
        self.fields = {}
        self.grouped_fields = {}
        if item_id == None:
            self.title("New rule monitor")
        self.geometry("1280x960")
        
        # Rule Fields
        rule_description_label = customtkinter.CTkLabel(self, text='Description', font=customtkinter.CTkFont(size=20, weight="bold"))
        rule_description_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        rule_description_entry = self.add_field('Rule_Description', tk.Entry, group='rf', auto_pos=False, width=100)
        rule_description_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        rule_monitor_label = customtkinter.CTkLabel(self, text='Monitor', font=customtkinter.CTkFont(size=20, weight="bold"))
        rule_monitor_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        rule_monitor_canvas = customtkinter.CTkCanvas(self)
        rule_monitor_canvas.grid(row=2, column=1)
        self.monitor_fields = 3
        self.add_rule_monitor_fields(rule_monitor_canvas)
        rule_monitor_canvas.bind("<Configure>", lambda event: self.resize_box(rule_monitor_canvas, event))
        plus_icon = get_plus_icon(self)
        rule_monitor_plus_button = tk.Button(rule_monitor_canvas, image=plus_icon, width=50, height=50, command=lambda: self.add_rule_monitor_fields(rule_monitor_canvas))
        rule_monitor_plus_button.image = plus_icon
        rule_monitor_canvas.create_window(10, 10, window=rule_monitor_plus_button, anchor=tk.NW)
        
        self.add_rule_conditon_fields()
        self.add_rule_operation_fields()

        
        if item_id == None:
            self.save_button = customtkinter.CTkButton(self, text="Create", command=self.create_and_close)
            self.cancel_button = customtkinter.CTkButton(self, text="Cancel", command=self.destroy)
            self.save_button.grid(row=len(self.fields) + 1, column=0, columnspan=1, pady=10)
            self.cancel_button.grid(row=len(self.fields) + 1, column=2, columnspan=1, pady=5)
        else:
            self.save_button = customtkinter.CTkButton(self, text="Save", command=self.save_and_close)
            self.cancel_button = customtkinter.CTkButton(self, text="Cancel", command=self.destroy)
            self.delete_button = customtkinter.CTkButton(self, text="Delete", command=self.destroy)
            self.save_button.grid(row=len(self.fields) + 1, column=0, columnspan=1, pady=10)
            self.cancel_button.grid(row=len(self.fields) + 1, column=1, columnspan=1, pady=5)
            self.delete_button.grid(row=len(self.fields) + 1, column=2, columnspan=1, pady=5)
    
    def add_rule_monitor_fields(self, master):
        field_1 = self.add_field('Monitor_SourcePath', customtkinter.CTkEntry, group='rmf', master=master, width=150)
        field_2 = self.add_field('Monitor_Subfolder', tk.Checkbutton, group='rmf', master=master)
        def askdir():
            selectedFolder = filedialog.askdirectory()
            field_1.delete(0, tk.END)
            field_1.insert(0, selectedFolder)
        select_button = customtkinter.CTkButton(self, text="Select Folder", command=askdir)
        y_position = self.monitor_fields * 30  
        master.create_window(10, y_position, window=field_1, anchor=tk.NW)
        master.create_window(200, y_position, window=select_button, anchor=tk.NW)
        master.create_window(10, y_position + 30, window=field_2, anchor=tk.NW)
        self.resize_box(master, None)
        self.monitor_fields = self.monitor_fields + 2
        
    def add_rule_conditon_fields(self):
        self.add_field('Condition_Operator', customtkinter.CTkEntry, label='Condition Operator', group='rcf')
        self.add_field('Condition_Base', customtkinter.CTkEntry, label='Condition Base', group='rcf')
        self.add_field('Condition_Operator', customtkinter.CTkEntry, label='Condition Operator', group='rcf')
        self.add_field('Condition_Value', customtkinter.CTkEntry, label='Condition Value', group='rcf')
        self.add_field('Value_Value', customtkinter.CTkEntry, label='Value', group='rcf')
        
    def add_rule_operation_fields(self):
        self.add_field('Operation_Action', customtkinter.CTkEntry, label='Operation Action', group='rof')
        self.add_field('Operation_ActionValue', customtkinter.CTkEntry, label='Operation Action Value', group='rof')
    
    def add_field(self, field_name, widget_class, master=None, value=None, label=None, group=None, auto_pos=True, **widget_kwargs):
        row = len(self.fields)
        if label:
            label_widget = tk.Label(self, text=label)
            label_widget.grid(row=row, column=0, padx=5, pady=5, sticky="e")
            self.fields[f"{field_name}_label"] = label_widget
        if master:
            widget = widget_class(master, **widget_kwargs)
        else:
            widget = widget_class(self, **widget_kwargs)
        if auto_pos:
            widget.grid(row=row, column=1, padx=5, pady=5, sticky="w")
        self.fields[field_name] = widget
        if group:
            if group not in self.grouped_fields:
                self.grouped_fields[group] = []

            self.grouped_fields[group].append(widget)
        return widget
        
    def initialize_rule(self, item_id):
        pass
    
    def create_and_close(self):
        description = self.grouped_fields['rf'][0].get()
        rule = self.adapter.send_command('create_rule', {'id': None, 'description': description})
        self.destroy()

    def save_and_close(self):
        self.tree.insert("", "end", values=(self.item_id, self.entry_name.get(), self.entry_age.get()))
        self.destroy()
        
    def resize_box(self, master, event):
        bbox = master.bbox(tk.ALL)
        master.config(width=bbox[2] + 10, height=bbox[3] + 10)

class RuleViewGUI(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.adapter = FolderServiceAdapter()
        self.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.setup_style()
        customtkinter.CTkLabel(self, text="Tag Screen", font=("Helvetica", 16)).pack()
        self.create_tags_table()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=25, bordercolor="#343638", borderwidth=0)
        style.map('Treeview', background=[('selected', '#22559b')])
        style.configure("Treeview.Heading", relief="flat")
        style.map("Treeview.Heading", background=[('active', '#3484F0')])
    
    def create_tags_table(self):
        columns = ("Id", "Active", "Description", "Paths monitored")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="browse", style="Treeview")
        self.setup_tree(self.tree, columns)
        rules = self.adapter.send_command_request('get_all_rules_aggregate')
        for rule in rules:
            self.tree.insert("", "end", values=(rule['id'], 'True', rule['description'], len(rule['rulemonitors'])), tags=("Clickable",))
        self.tree.tag_bind("Clickable", "<ButtonRelease-1>", self.on_item_click)
        self.tree.pack(padx=10, pady=20, fill=tk.BOTH, expand=True)
        self.setup_buttons(self.tree)
        
    def on_item_click(self, event):
        item = self.tree.focus() 
        if item:
            RuleViewSingleWindowGUI(self, self.tree, item)

    def setup_tree(self, tree, columns):
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=150)

    
    def setup_buttons(self, tree):
        add_button = customtkinter.CTkButton(self, text="New Rule monitor", command=lambda: RuleViewSingleWindowGUI(self, self.tree))
        add_button.pack(side=tk.LEFT, padx=10)

    
    def trigger_move(self, tree):
        selected_item = tree.selection()
        if selected_item:
            current_data = tree.item(selected_item, "values")
            self.master.folder_service_adapter.send_command('trigger', {'source_path': current_data[1], 'tags': current_data[2], 'target_path': current_data[3]})
            
    def _send_tag_path(self, tag_path, command):
        request_body = {
            "id": str(tag_path['id']),
            "source_path": tag_path['sourcepath'], 
            "tags": tag_path['tags'], 
            "target_path": tag_path['targetpath']
        }
        self.master.folder_service_adapter.send_command(command, request_body)
            
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
            self.master.folder_service_adapter.send_command('add', {
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
        self.master.folder_service_adapter.send_command('add', {
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
        self.master.folder_service_adapter.send_command('delete', {
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
            self.master.folder_service_adapter.send_command('update', {
                "id": str(id),
                "source_path": source_path, 
                "tags": tags, 
                "target_path": target_path
            })