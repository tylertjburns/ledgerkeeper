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
        return name in cls._member_names_

    @classmethod
    def has_value(cls, value):
        return value in set([item.value for item in cls])

class TransactionSource(Enum):
    PNC = 1
    BARCLAYCARDUS = 2
    ARCHIVE = 3

    @classmethod
    def has_name(cls, name):
        return name in cls._member_names_

    @classmethod
    def has_value(cls, value):
        return value in set(item.value for item in cls)

class TransactionStatus(Enum):
    UNHANDLED = 1
    HANDLED = 2
    DUPLICATE = 3
    DENIED = 4
    SPLIT = 5

    @classmethod
    def has_name(cls, name):
        return name in cls._member_names_

    @classmethod
    def has_value(cls, value):
        return value in set([item.value for item in cls])

class TransactionSplitType(Enum):
    PERCENTAGE = 1
    DOLLAR = 2

    @classmethod
    def has_name(cls, name):
        return name in cls._member_names_

    @classmethod
    def has_value(cls, value):
        return value in set([item.value for item in cls])

class AccountType(Enum):
    PERSONAL = 1
    BUSINESS = 2

    @classmethod
    def has_name(cls, name):
        return name in cls._member_names_

    @classmethod
    def has_value(cls, value):
        return value in set([item.value for item in cls])

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
    NA = 22

    @classmethod
    def has_name(cls, name):
        return name in cls._member_names_

    @classmethod
    def has_value(cls, value):
        return value in set([item.value for item in cls])

class HandleTransactionMethod(Enum):
    SPLIT = 1
    APPROVE = 2
    DENY = 3
    DUPLICATE = 4

    @classmethod
    def has_name(cls, name):
        return name in cls._member_names_

    @classmethod
    def has_value(cls, value):
        return value in set([item.value for item in cls])

class PlotType(Enum):
    HISTORY_BY_CATEGORY = 1
    PROJECTED_FINANCE = 2

    @classmethod
    def has_name(cls, name):
        return name in cls._member_names_

    @classmethod
    def has_value(cls, value):
        return value in set([item.value for item in cls])

if __name__ == "__main__":
    enum = TransactionSource
    print(enum.has_value(1))