
from abc import ABC, abstractmethod
from typing import Dict

class UserIteractionManager(ABC):
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
    def request_filepath(self):
        pass

    @abstractmethod
    def pretty_print_items(self, items, title=None):
        pass

    @abstractmethod
    def request_transaction_action(self):
        pass

    @abstractmethod
    def plot_request_action(self):
        pass