from abc import ABC, abstractmethod
from ledgerkeeper.mongoData.account import Account
from ledgerkeeper.enums import SpendCategory

class IBucketUpdater(ABC):
    @abstractmethod
    def update_bucket(self,
                      account: Account, bucketName: str,
                      priority: int = None,
                      due_day_of_month: int = None,
                      spend_category: SpendCategory = None,
                      base_budget_amount: float = None,
                      perc_budget_amount: float = None,
                      waterfall_amount: float = None,
                      saved_amount: float = None,
                      percent_of_income_adjustment_amount: float = None,
                      ):
        pass