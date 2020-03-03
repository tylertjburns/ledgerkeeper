from abstracts.userInteractionManager import UserIteractionManager
import time
import pandas as pd
import json
from enum import Enum
from dateutil import parser
import datetime

from typing import Dict

import tkinter
import tkinter.filedialog as fd


class CliInteractionManager(UserIteractionManager):
    def notify_user(self, text: str):
        print(text)
        time.sleep(1)

    def request_string(self, prompt: str):
        return input(prompt)

    def request_int(self, prompt: str):
        while True:
            ret = self._int_tryParse(input(prompt))
            if ret:
                return ret
            else:
                self.notify_user("Invalid Integer...")

    def _int_tryParse(self, value):
        try:
            return int(value)
        except:
            return False

    def request_enum(self, enum):
        while True:
            if issubclass(enum, Enum):
                print(f"Enter {enum.__name__}:")
                for i in enum:
                    print(f"{i.value} -- {i.name}")
                inp = input("")

                enum_num = self._int_tryParse(inp)
                if enum_num and enum.has_value(enum_num):
                    return enum(enum_num).name
                elif not enum_num and enum.has_name(inp):
                    return inp
                else:
                    print(f"Invalid Entry...")

            else:
                raise TypeError(f"Input must be of type Enum but {type(enum)} was provided")


    def request_float(self, prompt: str):
        while True:
            try:
                return float(input(prompt))
            except:
                self.notify_user("invalid float format")

    def request_guid(self, prompt: str):
        while True:
            inp = input(prompt)
            if (len(inp)) == 24:
                return inp
            else:
                self.notify_user("Invalid Guid...")



    def request_date(self):

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

    def request_from_dict(self, selectionDict: Dict[int, str], prompt=None) -> str:
        if prompt is None:
            prompt = ""

        print(prompt)
        for key in selectionDict:
            print(f"{key} -- {selectionDict[key]}")

        while True:
            inp = self._int_tryParse(input(""))

            if inp and selectionDict.get(inp, None) is not None:
                return selectionDict[inp]
            else:
                print("Invalid Entry")


    def request_filepath(self):
        root = tkinter.Tk()
        in_path = fd.askopenfilename()
        root.destroy()

        return in_path

    def pretty_print_items(self, items, title=None):
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

    def request_transaction_action(self):
        print("What do you want to do with this transaction?")

        print("[A]pprove")
        print("[D]eny")
        print("[S]plit")
        print("Mark D[U]plicate")
        print("[B]ack to main menu")
        print("")
        return self.request_string("").upper()

    def plot_request_action(self):
        print("What do you want to plot?")

        print("[H]istory by Category")
        print("[B]ack to main menu")
        print("")
        return input("").upper()
