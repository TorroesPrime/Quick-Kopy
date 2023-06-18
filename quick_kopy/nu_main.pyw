import json
import os
import sys
import tkinter as tk
from functools import partial
from pathlib import Path
from tkinter import ttk
from tkinter.colorchooser import askcolor

from PIL import Image, ImageTk

config_name = 'myapp.cfg'
global APP_DIR, user_info, settings, default_settings, DEBUG
# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    APP_DIR = Path(sys.executable).parent
else:
    APP_DIR = Path(__file__).parent

DATA_DIR = APP_DIR / 'data'
DEFAULT_JSON = DATA_DIR / 'default.json'
USER_JSON = DATA_DIR / 'user.json'
GERMANNA_LOGO = DATA_DIR / 'Germanna-Logo-Red.png'
APP_ICON = DATA_DIR / 'icon.ico'

DEBUG = False
executable_path = sys.argv[0]
# Get the directory containing the executable file
# os.chdir(APP_DIR)
user_info = {}
default_settings = {"font": "Arial",
            "font_size": 12,
            "main bg": "#34363b",
            "bg": "#ffffff",
            "fg": "#000000",
            "width": 350,
            "height": 200,
            "title": "Germanna ACE Quick Copy",
            "layout":None,
            "button font": "Arial",
            "button font size": 16,
            "button bg": "#ffffff",
            "button fg": "#000000",
            "button padding x": 5,
            "button padding y": 5,
            "button font":(),
            "button size":25,
            "label font":"Arial",
            "label size":16,
            "frame bg": "#ffffff"}
system_fonts = [
    "Arial",
    "Helvetica",
    "Verdana",
    "Tahoma",
    "Times New Roman",
    "Georgia",
    "Courier New",
    "Monaco",
]

settings = {}

def gen_clean_files():
    global APP_DIR
    with open(DEFAULT_JSON, 'w') as f:
        json.dump(default_settings, f, indent=4)
    with open(USER_JSON, 'w') as f:
        json.dump({"settings": default_settings, "user items":{}}, f, indent=4)

def load_user_file(override=False):
    global default_settings, user_info, settings,DEBUG
    with open(DEFAULT_JSON) as f:
        default_settings = json.load(f)
        if DEBUG:
            print("Len: ", len(default_settings))
    if not override:
        if os.path.exists(USER_JSON):
            with open(USER_JSON) as f:
                set_data = json.load(f)
                settings = set_data["settings"]
                user_info = set_data["user items"]
        else:
            open(USER_JSON, "w").close()
            settings = default_settings
    else:
        open(USER_JSON, "w").close()
        settings = default_settings

def save_user_file(override=False):
    global user_info, settings, default_settings, APP_DIR
    with open(USER_JSON, 'w') as f:
        set_Data = default_settings if override else settings
        json.dump({"settings": set_Data, "user items":user_info}, f, indent=4)

class remove_item_window():
    global user_info,settings,default_settings,APP_DIR

    def __init__(self,root) -> None:
        self.root = tk.Toplevel(root)
        self.root.grab_set()
        self.root.title("Remove item")
        self.root.geometry("275x250")
        self.root.resizable(False,False)
        self.root.configure(bg=settings["main bg"])
        self.root.iconbitmap(APP_ICON)
        name_frame = tk.Frame(self.root,bg=settings["bg"],relief="groove",bd=2)
        main_canvas = tk.Canvas(self.root)
        main_canvas.grid(row=0,column=0,padx=5,pady=5,sticky="nsew")
        scrollbar = tk.Scrollbar(self.root, command=main_canvas.yview)
        scrollbar.grid(row=0,column=1,sticky="nsew")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        self.inner_frame = tk.Frame(main_canvas)
        main_canvas.create_window(0, 0, window=self.inner_frame, anchor='nw')
        main_canvas.bind_all("<MouseWheel>", lambda event: main_canvas.\
                             yview_scroll(int(-1*(event.delta/120)), "units"))
        self.draw_items()

    def draw_items(self):
        for widg in self.inner_frame.winfo_children():
            widg.destroy()
        if len(user_info) == 0:
            tk.Label(self.inner_frame,text="No items to remove",\
                    bg=settings["bg"],fg=settings["fg"],\
                    font=(settings["label font"],settings["label size"]))\
                    .pack(fill="x",expand=True)
        else:
            for item in user_info:
                tk.Button(self.inner_frame,text=item,command=partial\
                (self.remove_item,item),bg=settings["button bg"],\
                fg=settings["button fg"],font=(settings["button font"]\
                ,settings["button font size"]),\
                padx=settings["button padding x"]).pack(fill="x",expand=True)

    def remove_item(self,item):
        user_info.pop(item)
        self.draw_items()
        save_user_file()

class about_window():
    def __init__(self,root) -> None:
        self.root = tk.Toplevel(root)
        self.root.grab_set()
        self.root.title("About")
        self.root.geometry("500x250")
        self.root.resizable(False,False)
        self.root.configure(bg=settings["main bg"])
        self.root.iconbitmap(APP_ICON)
        image_path =Image.open(GERMANNA_LOGO)
        image_path = image_path.resize((350,73),Image.LANCZOS)
        germanna_logo = ImageTk.PhotoImage(image_path)
        a = tk.Label(self.root,image=germanna_logo)
        a.image = germanna_logo
        a.pack()
        tk.Label(self.root,text="Copyright: Michael G. Cividanes\nJune, 2023\
                 \nAll rights reserved.\nContact: \
                Michael.cividanes2010@gmail.com",fg=settings["fg"],\
                font=(settings["label font"],12)).pack(fill="x",expand=True)
        tk.Button(self.root,text="Close",command=self.close_window).pack()

    def close_window(self):
        self.root.destroy()

class settings_window():
    global user_info,settings,default_settings,APP_DIR

    def __init__(self,root) -> None:
        self.root = tk.Toplevel(root)
        self.root.grab_set()
        self.root.title("Settings")
        self.root.geometry("330x330")
        self.root.resizable(False,False)
        self.root.configure(bg=settings["bg"])
        self.root.iconbitmap(APP_ICON)
        self.mainframe = tk.Frame(self.root,bg=settings["bg"],relief="groove"\
            ,bd=2)
        self.mainframe.pack()
        self.font_clr_btn = tk.Button(self.mainframe,text=" ",\
            command=self.font_color,bg=settings["fg"],\
            fg=settings["fg"],padx=settings["button padding x"])
        self.font_clr_btn.grid(row=0,column=0,padx=5,pady=5)
        tk.Label(self.mainframe,text="Font Color",bg=settings["bg"],\
            fg=settings["fg"],font=(settings["label font"],12))\
            .grid(row=0,column=1,padx=5,pady=5)
        self.bg_clr_btn = tk.Button(self.mainframe,text=" ",\
            command=self.bg_color,bg=settings["bg"],\
            fg=settings["bg"],padx=settings["button padding x"])
        self.bg_clr_btn.grid(row=1,column=0,padx=5,pady=5)
        tk.Label(self.mainframe,text="Button BG",bg=settings["bg"],\
            fg=settings["fg"],font=(settings["label font"],12)).grid(row=1,\
            column=1,padx=5,pady=5)
        self.win_bg_clr_btn = tk.Button(self.mainframe,text=" ",\
            command=self.window_bg,bg=settings["frame bg"],\
            fg=settings["frame bg"],padx=settings["button padding x"])
        self.win_bg_clr_btn.grid(row=2,column=0,padx=5,pady=5)
        tk.Label(self.mainframe,text="Window BG",bg=settings["bg"],\
            fg=settings["fg"],font=(settings["label font"],12)).grid(\
            row=2,column=1,padx=5,pady=5)
        tk.Label(self.mainframe,text="font",bg=settings["bg"],fg=settings["fg"]\
        ,font=(settings["label font"],12)).grid(row=3,column=0,padx=5,pady=5)
        self.font = ttk.Combobox(self.mainframe,values=system_fonts,\
            state="readonly")
        self.font.set(settings["font"])
        self.font.grid(row=3,column=1,padx=5,pady=5)
        tk.Label(self.mainframe,text="font size",bg=settings["bg"],\
            fg=settings["fg"],font=(settings["label font"],12)).\
            grid(row=4,column=0,padx=5,pady=5)
        self.font_size = ttk.Combobox(self.mainframe,values=\
            [8,10,12,14,16,18,20,22,24,26,28,30],state="readonly")
        self.font_size.set(settings["font_size"])
        self.font_size.grid(row=4,column=1,padx=5,pady=5)
        tk.Label(self.mainframe,text="This is what buttons will look like next \
            time you launch QuikKopy",bg=settings["bg"],fg=settings["fg"],\
            font=(settings["label font"],12),wraplength=250).grid(row=5,column=0,\
            padx=5,pady=5,columnspan=2)
        self.btn_demo = tk.Button(self.mainframe,text="Demo",\
            bg=settings["button bg"],fg=settings["button fg"],\
            font=(settings["button font"],settings["button font size"]),\
            padx=settings["button padding x"])
        self.btn_demo.grid(row=6,column=0,padx=5,pady=5,columnspan=2)
        self.restor_btn = tk.Button(self.root,text="Restore Defaults",\
            command=self.restore_defaults,padx=10)
        self.restor_btn.pack(side="left")
        self.mainmenu_btn = tk.Button(self.root,text="Go to main menu",\
            command=self.restore_defaults,padx=10)
        self.mainmenu_btn.pack(side="left")
        self.cancel_btn = tk.Button(self.root,text="Restore Defaults",\
            command=self.restore_defaults,padx=10)
        self.cancel_btn.pack(side="left")
        self.root.bind("<Destroy>",lambda event: save_user_file())

    def restore_defaults(self):
        global settings
        settings = default_settings
        self.btn_demo.configure(fg=settings["fg"])
        self.font_clr_btn.configure(bg=settings["fg"])
        self.btn_demo.configure(bg=settings["button bg"])
        self.bg_clr_btn.configure(bg=settings["button bg"])
        self.mainframe.configure(bg=settings["frame bg"])
        self.win_bg_clr_btn.configure(bg=settings["frame bg"])
        self.update_label()

    def font_color(self):
        settings["fg"] = askcolor()[1]
        self.btn_demo.configure(fg=settings["fg"])
        self.font_clr_btn.configure(bg=settings["fg"])
        self.update_label()
        save_user_file()

    def bg_color(self):
        settings["button bg"] = askcolor()[1]
        self.btn_demo.configure(bg=settings["button bg"])
        self.bg_clr_btn.configure(bg=settings["button bg"])
        self.update_label()
        save_user_file()

    def window_bg(self):
        settings["main bg"] = askcolor()[1]
        self.mainframe.configure(bg=settings["main bg"])
        self.win_bg_clr_btn.configure(bg=settings["main bg"])
        save_user_file()

    def update_label(self):
        for widg in self.mainframe.winfo_children():
            if isinstance(widg,tk.Label):
                widg.configure(bg=settings["bg"],fg=settings["fg"],\
                font=(settings["label font"],12))

class add_item_window():
    global user_info,settings,default_settings,APP_DIR

    def __init__(self,root) -> None:
        self.root = tk.Toplevel(root)
        self.root.grab_set()
        self.root.title("Add item")
        self.root.geometry("325x375")
        self.root.resizable(False,False)
        self.root.configure(bg=settings["bg"])
        self.root.iconbitmap(APP_ICON)
        name_frame = tk.Frame(self.root,bg=settings["bg"],relief="groove",bd=2)
        name_frame.grid(row=0,column=0,padx=5,pady=5,sticky="nsew",\
            columnspan=2)
        tk.Label(name_frame,text="Name",bg=settings["bg"],\
            fg=settings["fg"],font=(settings["label font"],\
            settings["label size"])).grid(row=0,column=0)
        self.item_Name = tk.Entry(name_frame,bg=settings["bg"],\
            fg=settings["fg"],font=(settings["label font"],\
            settings["label size"]))
        self.item_Name.grid(row=0,column=1)
        item_content = tk.Frame(self.root,bg=settings["bg"],\
            relief="groove",bd=2)
        item_content.grid(row=1,column=0,padx=5,pady=5,sticky="nsew",\
            columnspan=2)
        tk.Label(item_content,text="Content",bg=settings["bg"],\
            fg=settings["fg"],font=(settings["label font"],\
            settings["label size"])).grid(row=1,column=0)
        self.item_Content = tk.Text(item_content,height=10,width=25,\
            bg=settings["bg"],fg=settings["fg"],\
            font=(settings["label font"],settings["label size"]))
        self.item_Content.grid(row=2,column=0,columnspan=2)
        tk.Button(self.root,text="Add",command=self.add_item).grid(row=3,\
            column=0,padx=5,pady=5)
        tk.Button(self.root,text="Cancel",command=self.clear).grid(row=3,\
            column=1,padx=5,pady=5)

    def clear(self):
        self.root.destroy()
        save_user_file()

    def add_item(self):
        user_info.update({self.item_Name.get():self.item_Content.get("1.0",\
            tk.END)})
        self.item_Name.delete(0,tk.END)
        self.item_Content.delete("1.0",tk.END)
        save_user_file()

class main_window():
    global user_info,settings,default_settings,APP_DIR

    def draw_menu(self,root):
        menubar = tk.Menu(root)
        menubar.add_command(label = "Add item", command= self.add_item)
        menubar.add_command(label = "Remove item", command= self.remove_item)
        menubar.add_command(label = "Settings", command= self.settings_window)
        menubar.add_command(label = "about", command= self.about)
        return menubar

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Germanna ACE Quick Copy")
        self.root.geometry(f"{settings['width']}x{settings['height']}")
        self.root.resizable(False,False)
        self.root.configure(bg=settings["bg"])
        self.root.iconbitmap(APP_ICON)
        self.mainframe = tk.Frame(self.root,bg=settings["bg"])
        self.mainframe.pack(fill="both",expand=True)
        self.root.config(menu=self.draw_menu(self.root))
        self.draw_item()
        total_height = self.needed_height(self.mainframe)
        self.root.geometry(f"{settings['width']}x{total_height}")
        if DEBUG:
            print("Total height:",total_height)

    def draw_item(self):
        for widg in self.mainframe.winfo_children():
            widg.destroy()
        if len(user_info.keys()) == 0:
            tk.Label(self.mainframe,text="You have no items in your repository.\
             Click 'Add item' to add an item.",wraplength=325,bg=settings["bg"]\
            ,fg=settings["fg"],font=(settings["label font"],14)).pack(fill="x",\
            expand=True)
        else:
            for item in user_info:
                a = tk.Button(self.mainframe,text=item,command=\
                    partial(self.copy_to_clipboard,user_info[item]),\
                    bg=settings["button bg"],fg=settings["button fg"],\
                    font=(settings["button font"],settings["button font size"])\
                    ,padx=settings["button padding x"])
                a.pack(fill="x",expand=True)
        total_height = self.needed_height(self.mainframe)
        self.root.geometry(f"{settings['width']}x{total_height}")

    def needed_height(self,frame):
        total_height = 0
        for _widg in frame.winfo_children():
            total_height += 64
        return total_height+28

    def copy_to_clipboard(self,text):
        self.root.clipboard_clear()  # Clear the clipboard
        self.root.clipboard_append(text)

    def add_item(self):
        a = add_item_window(self.root)
        a.root.bind("<Destroy>",lambda event: self.draw_item())

    def remove_item(self):
        a = remove_item_window(self.root)
        a.root.bind("<Destroy>",lambda event: self.draw_item())

    def settings_window(self):
        a = settings_window(self.root)

    def about(self):
        a = about_window(self.root)

load_user_file()
app = main_window()
app.root.mainloop()
