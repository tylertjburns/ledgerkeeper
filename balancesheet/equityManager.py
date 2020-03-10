import balancesheet.mongoData.equities_data_service as dsvce
from userInteraction.abstracts.userInteractionManager import UserIteractionManager
import ledgerkeeper.mongoData.account_data_service as dsvca
from balancesheet.enums import EquityClass, AssetType, LiabiltyType, EquityTimeHorizon, EquityStatus, EquityContingency
import plotter as plot

class EquityManager():
    def __init__(self, user_notification_system: UserIteractionManager):
        self.uns = user_notification_system


    def add_equity(self):
        name = self.uns.request_string("Name: ")
        description = self.uns.request_string("Description: ")
        accountName = self.uns.request_from_dict(dsvca.accounts_as_dict())
        equityClass = self.uns.request_enum(EquityClass)
        if equityClass == EquityClass.ASSET:
            equityType = self.uns.request_enum(AssetType)
        elif equityClass == EquityClass.LIABILITY:
            equityType = self.uns.request_enum(LiabiltyType)
        else:
            raise Exception(f"Unknown equity class: {equityClass.name}")

        interestRate = self.uns.request_float("Interest Rate: ")
        equityTimeHorizon = self.uns.request_enum(EquityTimeHorizon)
        equityStatus = self.uns.request_enum(EquityStatus)
        equityContingency = self.uns.request_enum(EquityContingency)

        equity = dsvce.enter_if_not_exists(name=name,
                                           description=description,
                                           accountId=str(dsvca.account_by_name(accountName).id),
                                           equityClass=equityClass,
                                           equityType=equityType,
                                           equityTimeHorizon=equityTimeHorizon,
                                           equityStatus=equityStatus,
                                           equityContingency=equityContingency,
                                           interestRate=interestRate)
    
        if equity is not None:
            self.uns.notify_user("Equity entered successfully!")

    def delete_equity(self):
        accountName = self.uns.request_from_dict(dsvca.accounts_as_dict())
        equityName = self.uns.request_from_dict(dsvce.equities_as_dict())

        dsvce.delete_equity(dsvca.account_by_name(accountName).id, equityName)

    def record_value(self):
        accountName = self.uns.request_from_dict(dsvca.accounts_as_dict())
        equityName = self.uns.request_from_dict(dsvce.equities_as_dict())
        year = self.uns.request_int("Year: ")
        month = self.uns.request_int("Month: ")
        value = self.uns.request_float("Value: ")


        account = dsvca.account_by_name(accountName)
        equity = dsvce.equity_by_account_and_name(str(account.id), equityName)
        if equity is None:
            raise Exception(f"Equity: {accountName} [{account.id}], {equityName} not found.")
        value = dsvce.record_value_on_equity(equity, year, month, value)
        
        if value is not None:
            self.uns.notify_user("Value Recorded successfully!")

    def print_value_snapshots(self, accountName=None):
        if accountName is None:
            accountName = self.uns.request_from_dict(dsvca.accounts_as_dict())

        account = dsvca.account_by_name(accountName)

        equities = dsvce.equities_by_account(account.id)

        if equities is None or len(equities) == 0:
            self.uns.notify_user(f"No Equities in account [{accountName}]")
            return

        self.uns.pretty_print_items(sorted(equities, key=lambda x: x.equityType),
                                    title="Equities Snapshots")

    def print_equities(self):
        self.uns.pretty_print_items(dsvce.query_equities("").to_json(), title="Equities")

    def print_balance_sheet(self):
        accountName = self.uns.request_from_dict(dsvca.accounts_as_dict())
        relevant_mos = self.uns.request_int("Number of past months: ")
        account = dsvca.account_by_name(accountName)
        
        data = dsvce.balance_sheet_over_time(relevant_months=relevant_mos, accountIds=[str(account.id)])
        
        self.uns.pretty_print_items(data)

    def plot_balance_over_time(self):
        relevant_mos = self.uns.request_int("Number of past months: ")
        accountName = self.uns.request_from_dict(dsvca.accounts_as_dict())
        account = dsvca.account_by_name(accountName)

        ax = plot.plot_assets_liabilities_worth_over_time(relevant_mos, accountIds=[str(account.id)])
        if ax is None:
            self.uns.notify_user("No Data to show...")
        # data = dsvce.balance_sheet_over_time(relevant_months=relevant_mos, accountIds=[str(account.id)])






