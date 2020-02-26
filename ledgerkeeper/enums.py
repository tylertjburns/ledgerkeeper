from enum import Enum



class TransactionTypes(Enum):
    APPLY_PAYMENT = 1
    APPLY_INCOME = 2
    MOVE_FUNDS = 3
    BALANCE_BANK = 4
    RECORD_EXPENSE = 5
    RECEIVE_REFUND = 6

    @classmethod
    def has_value(cls, value):
        return value in TransactionTypes._member_names_

class TransactionSource(Enum):
    PNC = 1,
    BARCLAYCARDUS = 2

    @classmethod
    def has_value(cls, value):
        return value in TransactionSource._member_names_

class CollectionType(Enum):
    LEDGER = 1,
    TRANSACTIONS = 2

    @classmethod
    def has_value(cls, value):
        return value in CollectionType._member_names_