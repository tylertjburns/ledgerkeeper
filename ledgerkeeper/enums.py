from enum import Enum


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
    ACCOUNTS = 3
    BUCKETS = 4

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

class SpendCategory(Enum):
    INVESTMENT = 1
    RENT_MORTGAGE =2
    GROCERIES =3
    CHARITY =4
    CARPAYMENT=5
    CARMAINT = 6
    FUN =7
    SPENDINGALLOWANCE=8
    OTHER=9
    LOANPAYMENT = 10
    FUEL = 11
    PHONE = 12
    UTILITIES = 13
    PETS = 14
    CARINSURANCE = 15
    LIFEINSURANCE = 16
    GENERALLIVINGEXPENSE = 17
    FOOD = 18
    VACATION = 19
    GENERALHOMEEXPENSE = 20
    MEDICAL = 21

    @classmethod
    def has_name(cls, name):
        return name in AccountType._member_names_

    @classmethod
    def has_value(cls, value):
        return value in set([item.value for item in AccountType])


if __name__ == "__main__":
    enum = TransactionSource
    print(enum.has_value(1))