from coreEnums import MyEnum

class TransactionTypes(MyEnum):
    APPLY_INCOME = 2  #Used for receiving funds into an account
    MOVE_FUNDS = 3  # Used for moving funds from one account/bucket to another
    BALANCE_BANK = 4  # Used for collecting un-allocated available funds into the waterfall
    RECORD_EXPENSE = 5  # Used for recording an expenditure
    RECEIVE_REFUND = 6  # Used if receiving a refund for a payment that had been recorded previously

class TransactionSource(MyEnum):
    PNC = 1
    BARCLAYCARDUS = 2
    ARCHIVE = 3
    MANUALENTRY = 4
    APPLICATION = 5

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
    CAR_PAYMENT=5
    CAR_MAINT = 6
    FUN =7
    SPENDING_ALLOWANCE=8
    OTHER=9
    LOAN_PAYMENT = 10
    FUEL = 11
    PHONE = 12
    UTILITIES = 13
    PETS = 14
    CAR_INSURANCE = 15
    LIFE_INSURANCE = 16
    GENERAL_LIVING_EXPENSE = 17
    FOOD = 18
    VACATION = 19
    GENERAL_HOME_EXPENSE = 20
    MEDICAL = 21
    CABLE_INTERNET = 22
    TRAVEL = 23
    NOEXPENSE = 24
    NOTAPPLICABLE = 25
    CAPITAL_PAYBACK = 26
    MAINTENANCE = 27
    ADMINISTRATION = 28
    CAPEX = 29
    CLOSING_COSTS = 30
    INSPECTION_APPRAISALS = 31
    PROPERTY_MANAGEMENT = 32



class HandleTransactionMethod(MyEnum):
    SPLIT = 1
    APPROVE = 2
    DENY = 3
    DUPLICATE = 4

class AccountStatus(MyEnum):
    ACTIVE = 1
    INACTIVE = 2

class DefaultBuckets(MyEnum):
    _DEFAULT = 1
    _CREDIT = 2
    _OTHER = 3
    _TAX_WITHOLDING = 4
    _PAY_WITH_REIMBURSEMENT = 5

class PaymentType(MyEnum):
    CREDIT = 1
    CASH = 2
    BANK = 3
    NOTAPPLICABLE = 4

class PaymentMethod(MyEnum):
    AUTO_WITHDRAW = 1
    AUTO_CREDIT = 2
    MANUAL = 3

if __name__ == "__main__":
    enum = SpendCategory

    print(SpendCategory['INVESTMENT'].name)
    print(enum.has_value(1))