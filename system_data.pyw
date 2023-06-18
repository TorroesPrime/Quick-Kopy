""" handles access to system data"""

from pathlib import Path
import os
import sys
import json

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    APP_DIR = Path(sys.executable).parent
else:
    APP_DIR = Path(os.path.abspath(__file__)).parent

DEFAULT_SETTINGS = {"win bg":"#d4d4d4",
            "pane bg":"#d4d4d4",
            "button bg":"#d4d4d4",
            "font color":"#000000",
            "font name":"Ariel",
            "padding x": 10,
            "padding y": 10,
            "font size": 12,
            "Title":"Germanna ACE Quick-Kopy",
            "icon":"icon.ico",
            }

class system_data:
    """ controls access to the system data while determining if a user.json 
    file exists. If one does exist, it is loaded and used. If not, the 
    default.json file is loaded and used.
    """
    def __init__(self):
        """ initializes the system data class. Checks if a user.json file exists, \
        if one does not exist, it then checks if default.json exists. If neither \
        exist, it generates a default.json file. and an empty user.json file \
        while loading the default.json file."""
        self._data = {}
        self._data_file = system_data().select_data()
        self._settings = self._data_file['settings']
        self._user_list = self._data_file['user_list']
    def generate_defaults(self):
        """generates a default.json"""
        with open(APP_DIR / 'data' / 'default.json', 'w') as f:
                data = {
                        "settings":self._settings,
                        "user_list":{}
                        }
                json.dump(self._data, f)
    def select_data():
        if Path(APP_DIR / 'data' / 'user.json').exists():
            file_name = APP_DIR / 'data' / 'user.json'
        elif Path(APP_DIR / 'data' / 'default.json').exists():
            file_name = APP_DIR / 'data' / 'default.json'
        else:
            self.generate_defaults()
            file_name = APP_DIR / 'data' / 'default.json'
        with open(APP_DIR / 'data' / 'user.json') as f:
            data = json.load(f)
        return data 
    
        