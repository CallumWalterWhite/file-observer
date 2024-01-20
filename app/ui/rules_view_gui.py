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
        self.item_id = item_id
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
        
        #Montior
        rule_monitor_label = customtkinter.CTkLabel(self, text='Monitor', font=customtkinter.CTkFont(size=20, weight="bold"))
        rule_monitor_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        rule_monitor_canvas = customtkinter.CTkCanvas(self)
        rule_monitor_canvas.grid(row=2, column=1)
        self.monitor_fields = 3
        self.subfolder_check_box = {}
        self.add_rule_monitor_fields(rule_monitor_canvas)
        rule_monitor_canvas.bind("<Configure>", lambda event: self.resize_box(rule_monitor_canvas, event))
        monitor_plus_icon = get_plus_icon(self)
        rule_monitor_plus_button = tk.Button(rule_monitor_canvas, image=monitor_plus_icon, width=50, height=50, command=lambda: self.add_rule_monitor_fields(rule_monitor_canvas))
        rule_monitor_plus_button.image = monitor_plus_icon
        rule_monitor_canvas.create_window(10, 10, window=rule_monitor_plus_button, anchor=tk.NW)
        
        #Condition
        rule_condition_label = customtkinter.CTkLabel(self, text='Conditions', font=customtkinter.CTkFont(size=20, weight="bold"))
        rule_condition_label.grid(row=4, column=0, padx=5, pady=15, sticky="w")
        rule_condition_canvas = customtkinter.CTkCanvas(self)
        rule_condition_canvas.grid(row=4, column=1)
        self.condition_fields = 3
        self.add_rule_conditon_fields(rule_condition_canvas)
        rule_condition_canvas.bind("<Configure>", lambda event: self.resize_box(rule_condition_canvas, event))
        condition_plus_icon = get_plus_icon(self)
        rule_canvas_plus_button = tk.Button(rule_condition_canvas, image=condition_plus_icon, width=50, height=50, command=lambda: self.add_rule_conditon_fields(rule_condition_canvas))
        rule_canvas_plus_button.image = condition_plus_icon
        rule_condition_canvas.create_window(10, 10, window=rule_canvas_plus_button, anchor=tk.NW)
        
        
        #Action
        rule_action_label = customtkinter.CTkLabel(self, text='Action', font=customtkinter.CTkFont(size=20, weight="bold"))
        rule_action_label.grid(row=6, column=0, padx=5, pady=15, sticky="w")
        rule_action_canvas = customtkinter.CTkCanvas(self)
        rule_action_canvas.grid(row=6, column=1)
        self.action_fields = 3
        self.add_rule_operation_fields(rule_action_canvas)
        rule_action_canvas.bind("<Configure>", lambda event: self.resize_box(rule_action_canvas, event))
        action_plus_icon = get_plus_icon(self)
        rule_canvas_plus_button = tk.Button(rule_action_canvas, image=action_plus_icon, width=50, height=50, command=lambda: self.add_rule_operation_fields(rule_action_canvas))
        rule_canvas_plus_button.image = action_plus_icon
        rule_action_canvas.create_window(10, 10, window=rule_canvas_plus_button, anchor=tk.NW)
        
        
        if item_id == None:
            self.save_button = customtkinter.CTkButton(self, text="Create", command=self.create_and_close)
            self.cancel_button = customtkinter.CTkButton(self, text="Cancel", command=self.destroy)
            self.save_button.grid(row=len(self.fields) + 1, column=0, columnspan=1, pady=10)
            self.cancel_button.grid(row=len(self.fields) + 1, column=2, columnspan=1, pady=5)
        else:
            self.save_button = customtkinter.CTkButton(self, text="Save", command=self.save_and_close)
            self.cancel_button = customtkinter.CTkButton(self, text="Cancel", command=self.destroy)
            self.delete_button = customtkinter.CTkButton(self, text="Delete", command=self.delete_and_close)
            self.save_button.grid(row=len(self.fields) + 1, column=0, columnspan=1, pady=10)
            self.cancel_button.grid(row=len(self.fields) + 1, column=1, columnspan=1, pady=5)
            self.delete_button.grid(row=len(self.fields) + 1, column=2, columnspan=1, pady=5)
    
    def add_rule_monitor_fields(self, master, suffix=None):
        field_1 = self.add_field(f'Monitor_SourcePath_{self.monitor_fields}', customtkinter.CTkEntry, sub_group=self.monitor_fields, group='rmf', master=master, width=150)
        sfcb_key = ('group_' + str(self.monitor_fields))
        self.subfolder_check_box[sfcb_key] = 0
        def click_subfolder_field(group):
            if self.subfolder_check_box[group] == 0:
                self.subfolder_check_box[group] = 1
            elif self.subfolder_check_box[group] == 1:
                self.subfolder_check_box[group] = 0
        field_2 = self.add_field(f'Monitor_Subfolder_{self.monitor_fields}', tk.Checkbutton, sub_group=self.monitor_fields, command=lambda: click_subfolder_field(sfcb_key), group='rmf', master=master)
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
        
    def add_rule_conditon_fields(self, master):
        field_1 = self.add_field(f'Condition_Operator_{self.condition_fields}', customtkinter.CTkOptionMenu, sub_group=self.condition_fields, master=master, group='rcf', values=['File Extension', 'File Name'])
        field_2 = self.add_field(f'Condition_Base_{self.condition_fields}', customtkinter.CTkOptionMenu, sub_group=self.condition_fields, master=master, group='rcf', values=['Is', 'Starts With', 'Ends With'])
        field_3 = self.add_field(f'Condition_Type_{self.condition_fields}', customtkinter.CTkOptionMenu, sub_group=self.condition_fields, master=master, group='rcf', values=['Text', 'Number'])
        field_4 = self.add_field(f'Condition_Value_{self.condition_fields}', customtkinter.CTkEntry, sub_group=self.condition_fields, master=master, group='rcf')

        y_position = self.condition_fields * 30  
        master.create_window(10, y_position, window=field_1, anchor=tk.NW)
        master.create_window(160, y_position, window=field_2, anchor=tk.NW)
        master.create_window(310, y_position, window=field_3, anchor=tk.NW)
        master.create_window(460, y_position, window=field_4, anchor=tk.NW)
        self.resize_box(master, None)
        self.condition_fields = self.condition_fields + 2
        
    def add_rule_operation_fields(self, master):
        field_1 = self.add_field(f'Operation_Action_{self.action_fields}', customtkinter.CTkOptionMenu, sub_group=self.action_fields, master=master, group='rof', values=['Move', 'Rename'])
        field_2 = self.add_field(f'Operation_Action_Value_{self.action_fields}', customtkinter.CTkEntry, sub_group=self.action_fields, group='rof', master=master)
        
        def askdir():
            selectedFolder = filedialog.askdirectory()
            field_2.delete(0, tk.END)
            field_2.insert(0, selectedFolder)
        select_button = customtkinter.CTkButton(self, text="Select Folder", command=askdir)
        y_position = self.action_fields * 30  
        master.create_window(10, y_position, window=field_1, anchor=tk.NW)
        master.create_window(160, y_position, window=field_2, anchor=tk.NW)
        master.create_window(310, y_position, window=select_button, anchor=tk.NW)
        self.resize_box(master, None)
        self.action_fields = self.action_fields + 2
    
    def add_field(self, field_name, widget_class, master=None, value=None, label=None, group=None, auto_pos=True, sub_group=None, **widget_kwargs):
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
                self.grouped_fields[group] = {}
            if sub_group:
                if sub_group not in self.grouped_fields[group]:
                    self.grouped_fields[group][sub_group] = {}
                self.grouped_fields[group][sub_group][field_name] = widget
            else:
                self.grouped_fields[group][field_name] = widget
        return widget
        
    def get_monitor_values(self):
        monitors = []
        rmf_ref = self.grouped_fields['rmf']
        monitor_keys = rmf_ref.keys()
        if len(monitor_keys) > 0:
            for key in monitor_keys:
                monitor_ref = rmf_ref[key]
                monitor_path = monitor_ref[f"Monitor_SourcePath_{key}"].get()
                sfcb_key = ('group_' + str(key))
                monitor_subfolder = self.subfolder_check_box[sfcb_key]
                monitors.append({
                    'sourcepath': monitor_path,
                    'subfolder': monitor_subfolder
                })
        else:
            raise Exception("Monitors can't be empty")
        return monitors
        
    def get_operation_values(self):
        operations = []
        rof_ref = self.grouped_fields['rof']
        operation_keys = rof_ref.keys()
        if len(operation_keys) > 0:
            for key in operation_keys:
                operation_ref = rof_ref[key]
                operation_action = operation_ref[f"Operation_Action_{key}"].get()
                operation_value = operation_ref[f"Operation_Action_Value_{key}"].get()
                operations.append({
                    'action': operation_action,
                    'action_value': operation_value
                })
        else:
            raise Exception("Operations can't be empty")
        return operations
    
        
    def get_conditions_values(self):
        conditions = []
        rcf_ref = self.grouped_fields['rcf']
        condition_keys = rcf_ref.keys()
        if len(condition_keys) > 0:
            for key in condition_keys:
                condition_ref = rcf_ref[key]
                condition_op = condition_ref[f"Condition_Operator_{key}"].get()
                condition_base = condition_ref[f"Condition_Base_{key}"].get()
                condition_type = condition_ref[f"Condition_Type_{key}"].get()
                condition_value = condition_ref[f"Condition_Value_{key}"].get()
                conditions.append({
                    'operator': condition_op,
                    'operator_base': condition_base,
                    'value_type': condition_type,
                    'value': condition_value
                })
        else:
            raise Exception("Conditions can't be empty")
        return conditions
        
    def initialize_rule(self, item_id):
        pass
    
    def create_and_close(self):
        description = self.grouped_fields['rf']['Rule_Description'].get()
        monitors = self.get_monitor_values()
        conditions = self.get_conditions_values()
        operations = self.get_operation_values()
        rule_data = self.adapter.send_command('create_rule', {'id': None, 'description': description, 'start': False})
        rule_id = rule_data['Id']
        for monitor in monitors:
            self.adapter.send_command('create_rule_monitor', {'id': None, 'ruleid': rule_id, 'sourcepath': monitor['sourcepath'], 'subfolder': monitor['subfolder']})
        for condition in conditions:
            self.adapter.send_command('create_rule_condition', {'id': None, 'ruleid': rule_id, 'operator': condition['operator'], 'operator_base': condition['operator_base'], 'value_type': condition['value_type'], 'value': condition['value']})
        for operation in operations:
            self.adapter.send_command('create_rule_operation', {'id': None, 'ruleid': rule_id, 'action': operation['action'], 'action_value': operation['action_value']})
        rule_data = self.adapter.send_command('start_rule', {'id': rule_id, 'description': description, 'start': True})
        self.destroy()
        
    def delete_and_close(self):
        self.adapter.send_command('delete_rule', {'id': self.item_id, 'description': '', 'start': False})
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