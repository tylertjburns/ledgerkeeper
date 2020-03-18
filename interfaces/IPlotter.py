from ledgerkeeper.mongoData.account import Account
import pandas as pd
from typing import List


from abc import ABC, abstractmethod
class IPlotter(ABC):

    @abstractmethod
    def _print_df(self,
                  df: pd.DataFrame):
        pass

    @abstractmethod
    def plot_history_by_category(self,
                                 recent_months: int, print_data=False, account: Account = None):
        pass

    @abstractmethod
    def plot_projected_finance(self,
                               relevant_past_mo: int, relevant_future_months: int, current_balance: float,
                               one_time_transactions=None, account: Account = None):
        pass

    @abstractmethod
    def plot_assets_liabilities_worth_over_time(self,
                                                relevant_months: int, print_data=False, accountIds: List[str] = None):
        pass

    @abstractmethod
    def show_plot(self,
                  axes, fig,
                  title="[Title]",
                  saveloc=None):
        pass

    @abstractmethod
    def plot_datetime(self,
                      df,
                      axes,
                      xaxis=None,
                      highlight=True,
                      weekend=5,
                      ylabel="Number of Visits",
                      facecolor='green',
                      alpha_span=0.2,
                      linestyle='-'):
        pass