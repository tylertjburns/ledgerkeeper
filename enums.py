from enum import Enum

class CollectionType(Enum):
    LEDGER = 1
    TRANSACTIONS = 2
    ACCOUNTS = 3
    BUCKETS = 4
    ENTITIES = 5
    ENTITY_VALUE_SNAPSHOTS = 6

    @classmethod
    def has_name(cls, name):
        return name in cls._member_names_

    @classmethod
    def has_value(cls, value):
        return value in set([item.value for item in cls])