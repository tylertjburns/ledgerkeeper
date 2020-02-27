from enum import Enum
from abc import ABC, abstractmethod


class TransactionTypes(Enum):
    APPLY_PAYMENT = 1
    APPLY_INCOME = 2
    MOVE_FUNDS = 3
    BALANCE_BANK = 4
    RECORD_EXPENSE = 5
    RECEIVE_REFUND = 6

    @classmethod
    def has_name(cls, name):
        return name in TransactionTypes._member_names_

    @classmethod
    def has_value(cls, value):
        return value in set([item.value for item in TransactionTypes])

class TransactionSource(Enum):
    PNC = 1
    BARCLAYCARDUS = 2

    @classmethod
    def has_name(cls, name):
        return name in TransactionSource._member_names_

    @classmethod
    def has_value(cls, value):
        return value in set(item.value for item in TransactionSource)

class TransactionStatus(Enum):
    UNHANDLED = 1
    HANDLED = 2
    DUPLICATE = 3
    DENIED = 4
    SPLIT = 5

    @classmethod
    def has_name(cls, name):
        return name in CollectionType._member_names_

    @classmethod
    def has_value(cls, value):
        return value in set([item.value for item in CollectionType])

class CollectionType(Enum):
    LEDGER = 1
    TRANSACTIONS = 2

    @classmethod
    def has_name(cls, name):
        return name in CollectionType._member_names_

    @classmethod
    def has_value(cls, value):
        return value in set([item.value for item in CollectionType])

class TransactionSplitType(Enum):
    PERCENTAGE = 1
    DOLLAR = 2

    @classmethod
    def has_name(cls, name):
        return name in TransactionSplitType._member_names_

    @classmethod
    def has_value(cls, value):
        return value in set([item.value for item in TransactionSplitType])

class AccountType(Enum):
    PERSONAL = 1
    BUSINESS = 2

    @classmethod
    def has_name(cls, name):
        return name in AccountType._member_names_

    @classmethod
    def has_value(cls, value):
        return value in set([item.value for item in AccountType])


if __name__ == "__main__":
    enum = TransactionSource
    print(enum.has_value(1))