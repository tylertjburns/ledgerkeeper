from enum import Enum

class TransactionTypes(Enum):
    APPLY_PAYMENT = 1
    APPLY_INCOME = 2
    MOVE_FUNDS = 3
    BALANCE_BANK = 4

    @classmethod
    def has_value(cls, value):
        return value in TransactionTypes._member_names_

class TransactionSource(Enum):
    PNC = 1,
    BARCLAYCARDUS = 2

    @classmethod
    def has_value(cls, value):
        return value in TransactionSource._member_names_
