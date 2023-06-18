from __future__ import annotations

import json
import tkinter as tk
from functools import cache
from tkinter import ttk
from tkinter.colorchooser import askcolor

from PIL import Image, ImageTk

from quick_kopy.config import (
    APP_ICON,
    COPYRIGHT_TEXT,
    DEBUG,
    DEFAULT_SETTINGS,
    GERMANNA_LOGO,
    USER_JSON,
    AppSettings,
    SystemFonts,
    UserSettings,
)


@cache
def load_config_file(override: bool = False) -> tuple[AppSettings, dict[str, str]]:
    if not override and USER_JSON.exists():
        set_data: UserSettings = json.loads(USER_JSON.read_text())
        settings = set_data["settings"]
        user_info = set_data["user_items"]
        return settings, user_info

    USER_JSON.write_text('')
    return DEFAULT_SETTINGS, {}


def save_config_file(settings: AppSettings | None = None,
                     user_info: dict[str, str] | None = None,
                     override: bool = False) -> None:

    temp_settings = DEFAULT_SETTINGS
    temp_user_info = {}

    if settings is None or user_info is None:
        temp_settings, temp_user_info = load_config_file()

    settings = settings if settings is not None else temp_settings
    user_info = user_info if user_info is not None else temp_user_info

    if override:
        settings = DEFAULT_SETTINGS

    USER_JSON.write_text(json.dumps({
        'settings': settings,
        'user_items': user_info,
    }, indent=4))
    load_config_file.cache_clear()


class RemoveItemWindow:

    def __init__(self: RemoveItemWindow, root: tk.Tk) -> None:
        settings, _ = load_config_file()

        self.root = tk.Toplevel(root)
        self.root.grab_set()
        self.root.title("Remove item")
        self.root.geometry("275x250")
        self.root.resizable(False, False)
        self.root.configure(bg=settings["main_bg"])
        self.root.iconbitmap(APP_ICON)

        main_canvas = tk.Canvas(self.root)
        main_canvas.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        scrollbar = tk.Scrollbar(self.root, command=main_canvas.yview)
        scrollbar.grid(row=0,column=1,sticky="nsew")

        main_canvas.configure(yscrollcommand=scrollbar.set)
        self.inner_frame = tk.Frame(main_canvas)
        main_canvas.create_window(0, 0, window=self.inner_frame, anchor='nw')
        main_canvas.bind_all(
            "<MouseWheel>",
            lambda event: main_canvas.yview_scroll(-1*(event.delta//120), "units"),
        )
        self.draw_items()

    def draw_items(self: RemoveItemWindow) -> None:
        settings, user_info = load_config_file()

        for widg in self.inner_frame.winfo_children():
            widg.destroy()

        if not user_info:
            tk.Label(
                self.inner_frame,
                text="No items to remove",
                bg=settings["bg"],
                fg=settings["fg"],
                font=(
                    settings["label_font"],
                    settings["label_size"],
                ),
            ).pack(fill="x", expand=True)
            return

        for title in user_info:
            tk.Button(
                self.inner_frame,
                text=title,
                command=lambda: self.remove_item(title),
                bg=settings["button_bg"],
                fg=settings["button_fg"],
                font=(
                    settings["button_font"],
                    settings["button_font_size"],
                ),
                padx=settings["button_padding_x"],
            ).pack(fill="x", expand=True)

    def remove_item(self: RemoveItemWindow, item: str):
        _, user_info = load_config_file()
        user_info.pop(item)
        save_config_file(user_info=user_info)
        self.draw_items()


class AboutWindow:
    def __init__(self: AboutWindow, root: tk.Tk) -> None:
        settings, _ = load_config_file()

        self.root = tk.Toplevel(root)
        self.root.grab_set()
        self.root.title("About")
        self.root.geometry("500x250")
        self.root.resizable(False, False)
        self.root.configure(bg=settings["main_bg"])
        self.root.iconbitmap(APP_ICON)

        with Image.open(GERMANNA_LOGO) as image_path:
            image_path = image_path.resize((350, 73), Image.LANCZOS)
            germanna_logo = ImageTk.PhotoImage(image_path)

        a = tk.Label(self.root, image=germanna_logo)
        a.image = germanna_logo
        a.pack()
        tk.Label(
            self.root,
            text=COPYRIGHT_TEXT,
            fg=settings["fg"],
            font=(settings["label_font"], 12),
        ).pack(fill="x", expand=True)

        tk.Button(self.root, text="Close", command=self.close_window).pack()

    def close_window(self):
        self.root.destroy()

class SettingsWindow:

    def __init__(self: SettingsWindow, root: tk.Tk) -> None:
        settings, _ = load_config_file()

        self.root = tk.Toplevel(root)
        self.root.grab_set()
        self.root.title("Settings")
        self.root.geometry("330x330")
        self.root.resizable(False, False)

        self.root.configure(bg=settings["bg"])
        self.root.iconbitmap(APP_ICON)

        self.mainframe = tk.Frame(
            self.root,
            bg=settings["bg"],
            relief="groove",
            bd=2,
        )
        self.mainframe.pack()

        self.font_clr_btn = tk.Button(
            self.mainframe,
            text=" ",
            command=self.font_color,
            bg=settings["fg"],
            fg=settings["fg"],
            padx=settings["button_padding_x"],
        )
        self.font_clr_btn.grid(row=0, column=0, padx=5, pady=5)

        tk.Label(
            self.mainframe,
            text="Font Color",
            bg=settings["bg"],
            fg=settings["fg"],
            font=(settings["label_font"], 12),
        ).grid(row=0, column=1, padx=5, pady=5)

        self.bg_clr_btn = tk.Button(
            self.mainframe,
            text=" ",
            command=self.bg_color,
            bg=settings["bg"],
            fg=settings["fg"],
            padx=settings["button_padding_x"],
        )
        self.bg_clr_btn.grid(row=1, column=0, padx=5, pady=5)

        tk.Label(
            self.mainframe,
            text="Button BG",
            bg=settings["bg"],
            fg=settings["fg"],
            font=(settings["label_font"], 12),
        ).grid(row=1, column=1, padx=5, pady=5)

        self.win_bg_clr_btn = tk.Button(
            self.mainframe,text=" ",
            command=self.window_bg,
            bg=settings["frame_bg"],
            fg=settings["frame_bg"],
            padx=settings["button_padding_x"],
        )
        self.win_bg_clr_btn.grid(row=2, column=0, padx=5, pady=5)

        tk.Label(
            self.mainframe,
            text="Window BG",
            bg=settings["bg"],
            fg=settings["fg"],
            font=(settings["label_font"], 12),
        ).grid(row=2, column=1, padx=5, pady=5)

        tk.Label(
            self.mainframe,
            text="font",
            bg=settings["bg"],
            fg=settings["fg"],
            font=(settings["label_font"], 12),
        ).grid(row=3, column=0, padx=5, pady=5)

        self.font = ttk.Combobox(
            self.mainframe,
            values=list(SystemFonts._value2member_map_),
            state="readonly",
        )
        self.font.set(settings["font"])
        self.font.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(
            self.mainframe,
            text="font size",
            bg=settings["bg"],
            fg=settings["fg"],
            font=(settings["label_font"], 12),
        ).grid(row=4, column=0, padx=5, pady=5)

        self.font_size = ttk.Combobox(
            self.mainframe,
            values=[8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30],
            state="readonly",
        )
        self.font_size.set(settings["font_size"])
        self.font_size.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(
            self.mainframe,
            text="This is what buttons will look like next time you launch QuickKopy",
            bg=settings["bg"],
            fg=settings["fg"],
            font=(settings["label_font"], 12),
            wraplength=250,
        ).grid(row=5, column=0, padx=5, pady=5, columnspan=2)

        self.btn_demo = tk.Button(
            self.mainframe,
            text="Demo",
            bg=settings["button_bg"],
            fg=settings["button_fg"],
            font=(
                settings["button_font"],
                settings["button_font_size"],
            ),
            padx=settings["button_padding_x"],
        )
        self.btn_demo.grid(row=6, column=0, padx=5, pady=5, columnspan=2)

        self.restor_btn = tk.Button(
            self.root,
            text="Restore Defaults",
            command=self.restore_defaults,
            padx=10,
        )
        self.restor_btn.pack(side="left")

        self.mainmenu_btn = tk.Button(
            self.root,
            text="Go to main menu",
            command=self.restore_defaults,
            padx=10,
        )
        self.mainmenu_btn.pack(side="left")

        self.cancel_btn = tk.Button(
            self.root,
            text="Restore Defaults",
            command=self.restore_defaults,
            padx=10,
        )
        self.cancel_btn.pack(side="left")


    def restore_defaults(self: SettingsWindow) -> None:
        save_config_file(settings=DEFAULT_SETTINGS)
        settings, _ = load_config_file()

        self.btn_demo.configure(fg=settings["fg"])
        self.font_clr_btn.configure(bg=settings["fg"])
        self.btn_demo.configure(bg=settings["button_bg"])
        self.bg_clr_btn.configure(bg=settings["button_bg"])
        self.mainframe.configure(bg=settings["frame_bg"])
        self.win_bg_clr_btn.configure(bg=settings["frame_bg"])
        self.update_label()

    def font_color(self: SettingsWindow) -> None:
        settings, _ = load_config_file()
        settings["fg"] = askcolor()[1]
        save_config_file(settings=settings)

        self.btn_demo.configure(fg=settings["fg"])
        self.font_clr_btn.configure(bg=settings["fg"])
        self.update_label()

    def bg_color(self: SettingsWindow) -> None:
        settings, _ = load_config_file()
        settings["button_bg"] = askcolor()[1]
        save_config_file(settings=settings)

        self.btn_demo.configure(bg=settings["button_bg"])
        self.bg_clr_btn.configure(bg=settings["button_bg"])
        self.update_label()

    def window_bg(self: SettingsWindow) -> None:
        settings, _ = load_config_file()
        settings["main_bg"] = askcolor()[1]
        save_config_file(settings=settings)

        self.mainframe.configure(bg=settings["main_bg"])
        self.win_bg_clr_btn.configure(bg=settings["main_bg"])

    def update_label(self: SettingsWindow) -> None:
        settings, _ = load_config_file()

        for widg in self.mainframe.winfo_children():
            if isinstance(widg, tk.Label):
                widg.configure(
                    bg=settings["bg"],
                    fg=settings["fg"],
                    font=(settings["label_font"], 12),
                )

class AddItemWindow:

    def __init__(self: AddItemWindow, root: tk.Tk) -> None:
        settings, _ = load_config_file()

        self.root = tk.Toplevel(root)
        self.root.grab_set()
        self.root.title("Add item")
        self.root.geometry("325x375")
        self.root.resizable(False, False)
        self.root.configure(bg=settings["bg"])
        self.root.iconbitmap(APP_ICON)

        name_frame = tk.Frame(self.root, bg=settings["bg"], relief="groove", bd=2)
        name_frame.grid(
            row=0,
            column=0,
            padx=5,
            pady=5,
            sticky="nsew",
            columnspan=2,
        )

        tk.Label(
            name_frame,
            text="Name",
            bg=settings["bg"],
            fg=settings["fg"],
            font=(
                settings["label_font"],
                settings["label_size"],
            ),
        ).grid(row=0, column=0)

        self.item_name = tk.Entry(
            name_frame,
            bg=settings["bg"],
            fg=settings["fg"],
            font=(
                settings["label_font"],
                settings["label_size"],
            ),
        )
        self.item_name.grid(row=0, column=1)

        item_content = tk.Frame(
            self.root,
            bg=settings["bg"],
            relief="groove",
            bd=2,
        )
        item_content.grid(
            row=1,
            column=0,
            padx=5,
            pady=5,
            sticky="nsew",
            columnspan=2,
        )

        tk.Label(
            item_content,
            text="Content",
            bg=settings["bg"],
            fg=settings["fg"],
            font=(
                settings["label_font"],
                settings["label_size"],
            ),
        ).grid(row=1, column=0)

        self.item_content = tk.Text(
            item_content,
            height=10,
            width=25,
            bg=settings["bg"],
            fg=settings["fg"],
            font=(
                settings["label_font"],
                settings["label_size"],
            ),
        )
        self.item_content.grid(row=2, column=0, columnspan=2)

        tk.Button(
            self.root,
            text="Add",
            command=self.add_item,
        ).grid(row=3, column=0, padx=5, pady=5)

        tk.Button(
            self.root,
            text="Cancel",
            command=self.clear,
        ).grid(row=3, column=1, padx=5, pady=5)

    def clear(self: AddItemWindow) -> None:
        self.root.destroy()

    def add_item(self: AddItemWindow) -> None:
        _, user_info = load_config_file()

        user_info.update({
            self.item_name.get(): self.item_content.get("1.0", tk.END),
        })
        self.item_name.delete(0, tk.END)
        self.item_content.delete("1.0", tk.END)
        save_config_file(user_info=user_info)

class MainWindow:

    def __init__(self) -> None:
        settings, _ = load_config_file()

        self.root = tk.Tk()
        self.root.title("Germanna ACE Quick Copy")
        self.root.geometry(f"{settings['width']}x{settings['height']}")
        self.root.resizable(False, False)
        self.root.configure(bg=settings["bg"])
        self.root.iconbitmap(APP_ICON)
        self.mainframe = tk.Frame(self.root, bg=settings["bg"])
        self.mainframe.pack(fill="both", expand=True)
        self.root.config(menu=self.draw_menu(self.root))
        self.draw_item()

        total_height = self.needed_height(self.mainframe)
        self.root.geometry(f"{settings['width']}x{total_height}")

        if DEBUG:
            print(f"Total height: {total_height}")

    def draw_menu(self: MainWindow, root: tk.Tk) -> tk.Menu:
        menubar = tk.Menu(root)
        menubar.add_command(label="Add item", command=self.add_item)
        menubar.add_command(label="Remove item", command=self.remove_item)
        menubar.add_command(label="Settings", command=self.settings_window)
        menubar.add_command(label="about", command=self.about)
        return menubar

    def draw_item(self: MainWindow) -> None:
        settings, user_info = load_config_file()

        for widg in self.mainframe.winfo_children():
            widg.destroy()

        if not user_info:
            tk.Label(
                self.mainframe,
                text="You have no items in your repository. Click 'Add item' to add an item.",
                wraplength=325,
                bg=settings["bg"],
                fg=settings["fg"],
                font=(settings["label_font"], 14),
            ).pack(fill="x", expand=True)

        else:
            for title, text in user_info.items():
                entry = tk.Button(
                    self.mainframe,
                    text=title,
                    command=lambda: self.copy_to_clipboard(text),
                    bg=settings["button_bg"],
                    fg=settings["button_fg"],
                    font=(
                        settings["button_font"],
                        settings["button_font_size"],
                    ),
                    padx=settings["button_padding_x"],
                )
                entry.pack(fill="x", expand=True)

        total_height = self.needed_height(self.mainframe)
        self.root.geometry(f"{settings['width']}x{total_height}")

    def needed_height(self: MainWindow, frame: tk.Frame) -> int:
        total_height = 64 * len(frame.winfo_children())
        return total_height + 28

    def copy_to_clipboard(self: MainWindow, text: str) -> None:
        self.root.clipboard_clear()
        self.root.clipboard_append(text)

    def add_item(self: MainWindow) -> None:
        child = AddItemWindow(self.root)
        child.root.bind("<Destroy>", lambda _event: self.draw_item())

    def remove_item(self: MainWindow) -> None:
        child = RemoveItemWindow(self.root)
        child.root.bind("<Destroy>", lambda _event: self.draw_item())

    def settings_window(self):
        SettingsWindow(self.root)

    def about(self):
        AboutWindow(self.root)

app = MainWindow()
app.root.mainloop()
