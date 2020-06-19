from coreEnums import MyEnum

class EquityClass(MyEnum):
    ASSET = 1
    LIABILITY = 2

class AssetType(MyEnum):
    REAL_ESTATE = 1
    CASH = 2
    ANNUITY = 3
    ACCOUNTS_RECEIVABLE = 4
    INVESTMENT_ACCOUNT = 5
    INVESTMENT_ACCOUNT_TAX_DEFFERRED = 6
    INVESTMENT_ACCOUNT_TAX_FREE = 7
    EQUIPMENT = 8
    ISSUED_LOAN = 9
    OTHER = 10


class LiabiltyType(MyEnum):
    ACCOUNTS_PAYABLE = 1
    CREDIT = 2
    PERSONAL_LOAN = 3
    STUDENT_LOAN = 4
    MORTGAGE = 5

class EquityTimeHorizon(MyEnum):
    SHORT_TERM = 1
    LONG_TERM = 2

class EquityContingency(MyEnum):
    CONTINGENT = 1
    FIXED = 2

class EquityStatus(MyEnum):
    OPEN = 1
    CLOSED = 2
