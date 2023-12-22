from .custom_dialog import CustomDialog
from .folder_selector import FolderSelector
from .custom_table import CustomTable
from ttkthemes import ThemedTk
import customtkinter

def show_custom_dialog(title, text, initialvalue=None, selectFolder=False):
    root = customtkinter.CTk()
    root.withdraw()

    dialog = CustomDialog(root, title, text, initialvalue, selectFolder)
    result = dialog.result

    root.destroy()

    return result

def show_folder_selector():
    root = customtkinter.CTk()
    root.withdraw()
    fl = FolderSelector(master=root)
    return fl.ask_directory()