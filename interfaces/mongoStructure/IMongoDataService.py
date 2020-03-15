from interfaces.mongoStructure import IMongoObject, IMongoObjectArgs
from typing import Dict, List
from abc import ABC, abstractmethod

class IMongoDataService(ABC):
    @abstractmethod
    def enter_new(self, args: IMongoObjectArgs) -> IMongoObject:
        pass

    @abstractmethod
    def enter_if_not_exists(self, args: IMongoObjectArgs) -> IMongoObject:
        pass

    @abstractmethod
    def delete(self, obj: IMongoObject) -> bool:
        pass

    @abstractmethod
    def object_by_name(self, name: str) -> IMongoObject:
        pass

    @abstractmethod
    def update_object(self, args: IMongoObjectArgs) -> IMongoObject:
        pass

    @abstractmethod
    def object_names_as_dict(self) ->  Dict[int, str]:
        pass

    @abstractmethod
    def query(self, query, objectNames: List[str] = None) -> List[IMongoObject]:
        pass

