from enums import MyEnum

class TransactionTypes(MyEnum):
    APPLY_PAYMENT = 1
    APPLY_INCOME = 2
    MOVE_FUNDS = 3
    BALANCE_BANK = 4
    RECORD_EXPENSE = 5
    RECEIVE_REFUND = 6

class TransactionSource(MyEnum):
    PNC = 1
    BARCLAYCARDUS = 2
    ARCHIVE = 3

class TransactionStatus(MyEnum):
    UNHANDLED = 1
    HANDLED = 2
    DUPLICATE = 3
    DENIED = 4
    SPLIT = 5

class TransactionSplitType(MyEnum):
    PERCENTAGE = 1
    DOLLAR = 2

class AccountType(MyEnum):
    PERSONAL = 1
    BUSINESS = 2

class SpendCategory(MyEnum):
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

class HandleTransactionMethod(MyEnum):
    SPLIT = 1
    APPROVE = 2
    DENY = 3
    DUPLICATE = 4

if __name__ == "__main__":
    enum = TransactionSource
    print(enum.has_value(1))