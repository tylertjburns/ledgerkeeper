from userInteraction.abstracts.userInteractionManager import UserIteractionManager
import time
import pandas as pd
import json
from enum import Enum
from dateutil import parser
import datetime

from typing import Dict

import tkinter
import tkinter.filedialog as fd

import mongoHelper
import pandasHelper

GOBACK = "X"

class CliInteractionManager(UserIteractionManager):
    def notify_user(self, text: str, delay_sec:int =1):
        print(text)
        time.sleep(delay_sec)

    def request_string(self, prompt: str):
        return input(prompt)

    def request_int(self, prompt: str):
        while True:
            inp = input(prompt).upper()
            if inp == "X":
                return None

            ret = self._int_tryParse(inp)
            if ret is not False:
                return ret
            else:
                self.notify_user("Invalid Integer...")

    def _int_tryParse(self, value):
        try:
            return int(value)
        except:
            return False

    def request_enum(self, enum, prompt:str = None):
        if prompt is not None:
            print(prompt)

        while True:
            if issubclass(enum, Enum):
                print(f"Enter {enum.__name__}:")
                for i in enum:
                    print(f"{i.value} -- {i.name}")
                print(f"{GOBACK} -- Go Back")
                inp = input("")

                if inp.upper() == GOBACK:
                    return None

                enum_num = self._int_tryParse(inp)
                if enum_num and enum.has_value(enum_num):
                    return enum(enum_num)
                elif not enum_num and enum.has_name(inp):
                    return enum[inp]
                else:
                    print(f"Invalid Entry...")

            else:
                raise TypeError(f"Input must be of type Enum but {type(enum)} was provided")


    def request_float(self, prompt: str, forcePos:bool = False):
        while True:
            try:
                inp = float(input(prompt))
                if forcePos and inp < 0:
                    raise Exception("Must be a positive number")

                return inp
            except Exception as e:
                self.notify_user(f"invalid float entry: {e}")

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
        print(f"{GOBACK} -- Go Back")
        inp = input("")

        if inp.upper() == GOBACK:
            return None

        while True:
            inp = self._int_tryParse(inp)

            if inp and selectionDict.get(inp, None) is not None:
                return selectionDict[inp]
            else:
                print("Invalid Entry")


    def request_open_filepath(self):
        root = tkinter.Tk()
        in_path = fd.askopenfilename()
        root.destroy()

        return in_path

    def request_save_filepath(self):
        root = tkinter.Tk()
        in_path = fd.asksaveasfilename()
        root.destroy()

        return in_path

    def request_you_sure(self, prompt=None):
        return self.request_from_dict({1: "Yes", 2: "No"}, prompt)

    def pretty_print_items(self, items, title=None):
        if type(items) == str:
            data = pd.io.json.json_normalize(json.loads(items))
        elif type(items) is list:
            data = mongoHelper.list_mongo_to_pandas(items)
        elif type(items) is pd.DataFrame:
            data = items
        else:
            raise NotImplementedError(f"Unhandled printable object {type(items)}")

        if title is None:
            title = ""
        else:
            title = title + "\n"

        print(f"{title}# of items {len(data)}")

        if len(data) > 0:
            pandasHelper.pretty_print_dataframe(data)


if __name__ == "__main__":
    helper = CliInteractionManager()
    # suc = helper._int_tryParse('0')
    suc = helper.request_int("prompt")
    # self._int_tryParse(input(prompt))
    print(suc)