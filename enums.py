from enum import Enum

class MyEnum(Enum):
    @classmethod
    def has_name(cls, name):
        return name in cls._member_names_

    @classmethod
    def has_value(cls, value):
        return value in set([item.value for item in cls])

class CollectionType(MyEnum):
    LEDGER = 1
    TRANSACTIONS = 2
    ACCOUNTS = 3
    BUCKETS = 4
    ENTITIES = 5
    ENTITY_VALUE_SNAPSHOTS = 6

class PlotType(MyEnum):
    HISTORY_BY_CATEGORY = 1
    PROJECTED_FINANCE = 2
    ASSET_LIABILITY_NET_OVER_TIME = 3

class ReportType(MyEnum):
    BALANCESHEETOVERTIME = 1