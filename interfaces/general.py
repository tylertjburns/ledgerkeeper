from abc import ABC, abstractmethod

class IIdGenerator(ABC):
    @abstractmethod
    def generate_new_id(self):
        pass
