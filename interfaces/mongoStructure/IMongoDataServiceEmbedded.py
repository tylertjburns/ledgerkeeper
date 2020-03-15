from interfaces.mongoStructure.IMongoDataService import IMongoDataService
from abc import ABC, abstractmethod

class IMongoDataServiceEmbedded(ABC, IMongoDataService):
    @abstractmethod
    def add_embedded_object(self):
        pass

    @abstractmethod
    def update_embedded_object(self):
        pass

    @abstractmethod
    def delete_embedded_object(self):
        pass
