"""Global configration options"""

import sys
from enum import Enum
from pathlib import Path
from typing import TypedDict


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


class SystemFonts(str, Enum):
    ARIAL = "Arial"
    COURIER_NEW = "Courier New"
    GEORGIA = "Georgia"
    HELVETICA = "Helvetica"
    MONACO = "Monaco"
    TAHOMA = "Tahoma"
    TIMES_NEW_ROMAN = "Times New Roman"
    VERDANA = "Verdana"


class DefaultSettings(TypedDict):
    pass


class UserSettings(DefaultSettings):
    pass


DEFAULT_SETTINGS = {
    "font": SystemFonts.ARIAL,
    "font_size": 12,
    "main bg": "#34363b",
    "bg": "#ffffff",
    "fg": "#000000",
    "width": 350,
    "height": 200,
    "title": "Germanna ACE Quick Copy",
    "layout": None,
    "button font": SystemFonts.ARIAL,
    "button font size": 16,
    "button bg": "#ffffff",
    "button fg": "#000000",
    "button padding x": 5,
    "button padding y": 5,
    "button font": (),
    "button size": 25,
    "label font": SystemFonts.ARIAL,
    "label size": 16,
    "frame bg": "#ffffff"
}
