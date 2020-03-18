
from abc import ABC, abstractmethod
from typing import Dict

class IAtomicInteractionHelper(ABC):

    @abstractmethod
    def notify_user(self, text: str):
        pass

    @abstractmethod
    def request_string(self, prompt: str):
        pass

    @abstractmethod
    def request_int(self, prompt: str):
        pass

    @abstractmethod
    def request_enum(self, enum):
        pass

    @abstractmethod
    def request_float(self, prompt: str):
        pass

    @abstractmethod
    def request_guid(self, prompt: str):
        pass

    @abstractmethod
    def request_date(self):
        pass

    @abstractmethod
    def request_from_dict(self, selectionDict: Dict[int, str], prompt=None) -> str:
        pass

    @abstractmethod
    def request_open_filepath(self):
        pass

    @abstractmethod
    def request_save_filepath(self):
        pass

    @abstractmethod
    def request_you_sure(self, items, prompt=None):
        pass



