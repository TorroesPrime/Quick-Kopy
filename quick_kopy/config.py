"""Global configration options"""

import sys
from enum import Enum
from pathlib import Path
from typing import TypedDict

APP_DIR = (
    Path(sys._MEIPASS)  # type: ignore[attr-defined]  # noqa: SLF001
    if getattr(sys, 'frozen', False)
    else Path(__file__).parent
)

DATA_DIR = APP_DIR / 'data'
DEFAULT_JSON = DATA_DIR / 'default.json'
GERMANNA_LOGO = DATA_DIR / 'Germanna-Logo-Red.png'
APP_ICON = DATA_DIR / 'icon.ico'

USER_JSON = Path(sys.executable).parent / 'user.json'

DEBUG = False


class SystemFonts(str, Enum):
    ARIAL = "Arial"
    COURIER_NEW = "Courier New"
    GEORGIA = "Georgia"
    HELVETICA = "Helvetica"
    MONACO = "Monaco"
    TAHOMA = "Tahoma"
    TIMES_NEW_ROMAN = "Times New Roman"
    VERDANA = "Verdana"


class AppSettings(TypedDict):
    font: SystemFonts
    font_size: int
    main_bg: str
    bg: str
    fg: str
    width: int
    height: int
    title: str
    layout: None
    button_font: SystemFonts
    button_font_size: int
    button_bg: str
    button_fg: str
    button_padding_x: int
    button_padding_y: int
    button_size: int
    label_font: SystemFonts
    label_size: int
    frame_bg: str


class UserSettings(TypedDict):
    settings: AppSettings
    user_items: dict[str, str]


DEFAULT_SETTINGS: AppSettings = {
    "font": SystemFonts.ARIAL,
    "font_size": 12,
    "main_bg": "#34363b",
    "bg": "#ffffff",
    "fg": "#000000",
    "width": 350,
    "height": 200,
    "title": "Germanna ACE Quick Copy",
    "layout": None,
    "button_font": SystemFonts.ARIAL,
    "button_font_size": 16,
    "button_bg": "#ffffff",
    "button_fg": "#000000",
    "button_padding_x": 5,
    "button_padding_y": 5,
    "button_size": 25,
    "label_font": SystemFonts.ARIAL,
    "label_size": 16,
    "frame_bg": "#ffffff",
}

COPYRIGHT_TEXT = """
Copyright: Michael G. Cividanes
June, 2023
All rights reserved.
Contact: Michael.cividanes2010@gmail.com
""".strip()
