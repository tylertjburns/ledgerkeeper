import time
import pandas as pd
import json
from enum import Enum
from dateutil import parser
import datetime

from typing import Dict

import tkinter
import tkinter.filedialog as fd


def _notify_user(text: str):
    print(text)
    time.sleep(1)


def _request_string(prompt: str):
    return input(prompt)

def _request_float(prompt: str):
    while True:
        try:
            return float(input(prompt))
        except:
            _notify_user("invalid float format")


def _request_guid(prompt: str):
    while True:
        inp = input(prompt)
        if (len(inp)) == 24:
            return inp
        else:
            _notify_user("Invalid Guid...")

def _request_int(prompt: str):
    while True:
        ret = _int_tryParse(input(prompt))
        if ret:
            return ret
        else:
            _notify_user("Invalid Integer...")


def _request_date():

    while True:
        inp = input("Enter date [Enter for current date]:")
        try:
            if inp == '':
                date_stamp = datetime.datetime.now()
                print(f"using: {date_stamp}")
            else:
                date_stamp = parser.parse(inp)
            break
        except:
            print("invalid date format")

    return date_stamp

def _request_from_dict(selectionDict: Dict[int, str], prompt = None) -> str:
    if prompt is None:
        prompt = ""

    print(prompt)
    for key in selectionDict:
        print (f"{key} -- {selectionDict[key]}")

    while True:
        inp = _int_tryParse(input(""))

        if inp and selectionDict.get(inp, None) is not None:
            return selectionDict[inp]
        else:
            print("Invalid Entry")

def _int_tryParse(value):
    try:
        return int(value)
    except:
        return False

def _request_enum(enum):
    while True:
        if issubclass(enum, Enum):
            print(f"Enter {enum.__name__}:")
            for i in enum:
                print(f"{i.value} -- {i.name}")
            inp = input("")

            enum_num = _int_tryParse(inp)
            if enum_num and enum.has_value(enum_num):
                return enum(enum_num).name
            elif not enum_num and enum.has_name(inp):
                return inp
            else:
                print(f"Invalid Entry...")

        else:
            raise TypeError(f"Input must be of type Enum but {type(enum)} was provided")


def _request_filepath():
    # Find File Path
    root = tkinter.Tk()
    in_path = fd.askopenfilename()
    # Close TKinter app
    root.destroy()

    return in_path


def _pretty_print_items(items, title=None):
    if type(items) == str:
        data = pd.io.json.json_normalize(json.loads(items))
    elif type(items) is list:
        jsonstr = "{ \"data\": ["
        for item in items:
            jsonstr += item.to_json() + ", "
        jsonstr = jsonstr[:-2] + "]}"
        jsonstr = json.loads(jsonstr)
        data = pd.io.json.json_normalize(jsonstr, record_path='data')
    else:
        raise NotImplementedError(f"Unhandled printable object {type(items)}")


    if title is None:
        title = ""
    else:
        title = title + "\n"

    print(f"{title}# of items {len(data)}")

    if len(data) > 0:
        with pd.option_context('display.max_rows', 500, 'display.max_columns', 2000, 'display.width', 250):
            print(data)