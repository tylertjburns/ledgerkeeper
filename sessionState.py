from ledgerkeeper.mongoData.account import Account


class SessionState():
    def __init__(self):
        self.account = None
        self.bank_balance = None
