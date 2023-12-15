import tkinter as tk
from tkinter import ttk, simpledialog
import customtkinter
from .custom_dialog import show_custom_dialog
import uuid
from .model import TagPath, Logs, db
from .watcher import Watcher
import os

class FolderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Folder Sorter Menu")
        self.root.geometry("1280x960")
        self.root.option_add("*Font", "helvetica 12")
        self.root.option_add("*TButton*relief", "flat")
        db.connect()
        db.create_tables([TagPath, Logs])
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                            #background="#2a2d2e",
                            #foreground="white",
                            rowheight=25,
                            #fieldbackground="#343638",
                            bordercolor="#343638",
                            borderwidth=0)
        style.map('Treeview', background=[('selected', '#22559b')])
    
        style.configure("Treeview.Heading",
                        #background="#565b5e",
                        #foreground="white",
                        relief="flat")
        style.map("Treeview.Heading",
                    background=[('active', '#3484F0')])

        self.home_frame = tk.Frame(root, bg="#ecf0f1")
        self.tags_frame = tk.Frame(root, bg="#ecf0f1")
        self.history_frame = tk.Frame(root, bg="#ecf0f1")
        self.refresh_w = True
        self.watches=[]
        self.show_screen()

    def show_screen(self):
        customtkinter.CTkLabel(self.home_frame, text="Tag Screen", font=("Helvetica", 16)).pack()
        self.tags_frame.pack(fill=tk.BOTH, expand=True)
        self.create_tags_table()
        self.refresh_watches()
        customtkinter.CTkLabel(self.home_frame, text="History Screen", font=("Helvetica", 16)).pack()
        self.history_frame.pack(fill=tk.BOTH, expand=True)
        self.create_history_table()

    def create_history_table(self):
        for widget in self.history_frame.winfo_children():
            widget.destroy()
        columns = ("Text", "Create Timestamp")
        tree = ttk.Treeview(self.history_frame, columns=columns, show="headings", selectmode="browse", style="Treeview")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=250)
        logs = Logs.select()

        for log in logs:
            tree.insert("", "end", values=(log.text, log.timestamp))

        tree.pack(padx=10, pady=20, fill=tk.BOTH, expand=True)


    def create_tags_table(self):
        columns = ("Id", "Source Path", "Tags", "Target Path")
        tree = ttk.Treeview(self.tags_frame, columns=columns, show="headings", selectmode="browse", style="Treeview")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=150)

        self.tags = TagPath.select()

        for row in self.tags:
            tree.insert("", "end", values=(row.id, row.sourcepath, row.tags, row.targetpath))

        tree.pack(padx=10, pady=20, fill=tk.BOTH, expand=True)

        add_button = customtkinter.CTkButton(self.tags_frame, text="Add", command=lambda: self.add_row(tree))
        add_button.pack(side=tk.LEFT, padx=10)

        remove_button = customtkinter.CTkButton(self.tags_frame, text="Remove", command=lambda: self.remove_row(tree))
        remove_button.pack(side=tk.LEFT, padx=10)

        edit_button = customtkinter.CTkButton(self.tags_frame, text="Edit", command=lambda: self.edit_row(tree))
        edit_button.pack(side=tk.LEFT, padx=10)

        auto_tag = customtkinter.CTkButton(self.tags_frame, text="Auto Tag", command=lambda: self.auto_tag(tree))
        auto_tag.pack(side=tk.LEFT, padx=10)

    def auto_tag(self, tree):
        source_path = show_custom_dialog("Auto Tag", "Enter Source Path:")
        target_path = show_custom_dialog("Auto Tag", "Enter Target path for tagging:")
        lowest_level_directories = []
        for root, dirs, files in os.walk(target_path):
            if not dirs:
                lowest_level_directories.append(root)
        for path in lowest_level_directories:
            base = os.path.basename(os.path.normpath(path))
            id = uuid.uuid4()
            tag = TagPath.create(id=id, sourcepath=source_path, tags=base, targetpath=path)
            tree.insert("", "end", values=(id, source_path, base, path))
        self.tags = TagPath.select()
        self.refresh_w = True
        self.refresh_watches()

    def add_row(self, tree):
        source_path = show_custom_dialog("Add Row", "Enter Source Path:")
        tags = show_custom_dialog("Add Row", "Enter Tags:")
        target_path = show_custom_dialog("Add Row", "Enter Target Path:")
        id = uuid.uuid4()
        tag = TagPath.create(id=id, sourcepath=source_path, tags=tags, targetpath=target_path)
        if source_path and tags and target_path:
            # Insert the new row into the table
            tree.insert("", "end", values=(id, source_path, tags, target_path))
        self.tags = TagPath.select()
        self.refresh_w = True
        self.refresh_watches()

    def remove_row(self, tree):
        selected_item = tree.selection()
        current_data = tree.item(selected_item, "values")
        id = current_data[0]
        TagPath.get(TagPath.id == id).delete_instance()
        if selected_item:
            tree.delete(selected_item)
        self.tags = TagPath.select()
        self.refresh_w = True
        self.refresh_watches()

    def edit_row(self, tree):
        selected_item = tree.selection()
        if selected_item:
            current_data = tree.item(selected_item, "values")
            id = current_data[0]
            source_path = show_custom_dialog("Edit Row", "Edit Source Path:", initialvalue=current_data[1])
            tags = show_custom_dialog("Edit Row", "Edit Tags:", initialvalue=current_data[2])
            target_path = show_custom_dialog("Edit Row", "Edit Target Path:", initialvalue=current_data[3])
            if source_path is not None and tags is not None and target_path is not None:
                # Update the row with the new data
                tree.item(selected_item, values=(current_data[0], source_path, tags, target_path))
            TagPath.update(sourcepath=source_path, tags=tags, targetpath=target_path).where(TagPath.id == id)
            self.tags = TagPath.select()
            self.refresh_w = True
            self.refresh_watches([current_data[0]])

    def refresh_watches(self, refresh_ids=[]):
        print('Refreshing watches')
        for tagpath in self.tags:
            id = tagpath.id
            if len(list(filter(lambda x: x.meta_id == id, self.watches))) == 0:
                watcher = Watcher(source=tagpath.sourcepath, tags=tagpath.tags, target=tagpath.targetpath, meta_id=id, callback=self.watcher_callback)
                self.watches.append(watcher)
                print('New watcher added')
            elif id in refresh_ids and len(list(filter(lambda x: x.meta_id == id, self.watches))) == 1:
                list(filter(lambda x: x.meta_id == id, self.watches))[0].stop()
                watcher = Watcher(source=tagpath.sourcepath, tags=tagpath.tags, target=tagpath.targetpath, meta_id=id, callback=self.watcher_callback)
                self.watches.append(watcher)
                print('Watcher updated')
        self.refresh_w = False

    def watcher_callback(self, logs):
        Logs.create(text=logs)
        self.create_history_table()
