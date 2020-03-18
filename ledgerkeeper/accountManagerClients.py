from userInteraction.interfaces.IFinanceInteraction import IFinanceInteraction
from userInteraction.financeCliInteraction import FinanceCliInteraction
from interfaces.IIdGenerator import IIdGenerator
from uuidGenerator import UuidGenerator
from ledgerkeeper.interfaces.ITransactionDataService import ITransactionDataService
from ledgerkeeper.mongoData.transactionDataService import TransactionDataService
from ledgerkeeper.interfaces.IAccountDataService import IAccountDataService
from ledgerkeeper.mongoData.accountDataService import AccountDataService
from ledgerkeeper.interfaces.ILedgerDataService import ILedgerDataService
from ledgerkeeper.mongoData.ledgerDataService import LedgerDataService
from ledgerkeeper.interfaces.ITransactionManager import ITransactionManager
from ledgerkeeper.transactionManager import TransactionManager
from interfaces.IPlotter import IPlotter
from plotter import Plotter
from mongoHelper import MongoHelper

class AccountManagerClients():
    def __init__(self,
                 interaction_system: IFinanceInteraction = None,
                 id_provider: IIdGenerator = None,
                 transaction_data_service: ITransactionDataService = None,
                 account_data_service: IAccountDataService = None,
                 ledger_data_service: ILedgerDataService=None,
                 transaction_manager: ITransactionManager=None,
                 mongo_helper: MongoHelper=None,
                 plotter: IPlotter=None
                 ):
        self._interaction_system = interaction_system
        self._id_provider = id_provider
        self._transaction_data_service = transaction_data_service
        self._account_data_service = account_data_service
        self._ledger_data_service = ledger_data_service
        self._transaction_manager = transaction_manager
        self._mongo_helper = mongo_helper
        self._plotter = plotter

    @property
    def interaction_system(self) -> IFinanceInteraction:
        if not self._interaction_system:
            self._interaction_system = FinanceCliInteraction()
        return self._interaction_system

    @property
    def id_provider(self) -> IIdGenerator:
        if not self._id_provider:
            self._id_provider = UuidGenerator()
        return self._id_provider

    @property
    def transaction_data_service(self) -> ITransactionDataService:
        if not self._transaction_data_service:
            self._transaction_data_service = TransactionDataService()
        return self._transaction_data_service

    @property
    def account_data_service(self) -> IAccountDataService:
        if not self._account_data_service:
            self._account_data_service = AccountDataService()
        return self._account_data_service

    @property
    def ledger_data_service(self) -> ILedgerDataService:
        if not self._ledger_data_service:
            self._ledger_data_service = LedgerDataService()
        return self._ledger_data_service

    @property
    def transaction_manager(self) -> ITransactionManager:
        if not self._transaction_manager:
            self._transaction_manager = TransactionManager()
        return self._transaction_manager

    @property
    def plotter(self) -> IPlotter:
        if not self._plotter:
            self._plotter = Plotter()
        return self._plotter

    @property
    def mongo_helper(self) -> MongoHelper:
        if not self._mongo_helper:
            self._mongo_helper = MongoHelper()
        return self._mongo_helper

