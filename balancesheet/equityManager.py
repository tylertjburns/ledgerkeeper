
from balancesheet.mongoData.equities import Equity
import balancesheet.mongoData.equities_data_service as dsvce
from userInteraction.abstracts.userInteractionManager import UserIteractionManager
import ledgerkeeper.mongoData.account_data_service as dsvca
from balancesheet.enums import EquityClass, AssetType, LiabiltyType, EquityTimeHorizon, EquityStatus, EquityContingency

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
            raise Exception("Unknown equity class")

        interestRate = self.uns.request_float("Interest Rate")
        equityTimeHorizon = self.uns.request_enum(EquityTimeHorizon)
        equityStatus = self.uns.request_enum(EquityStatus)
        equityContingency = self.uns.request_enum(EquityContingency)

        dsvce.enter_if_not_exists(name=name,
                                  description=description,
                                  accountId=dsvca.account_by_name(accountName).id,
                                  equityClass=equityClass,
                                  equityType=equityType,
                                  equityTimeHorizon=equityTimeHorizon,
                                  equityStatus=equityStatus,
                                  equityContingency=equityContingency,
                                  interestRate=interestRate)

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
        dsvce.record_value_on_equity(dsvce.equity_by_account_and_name(account.id, equityName), year, month, value)

    def print_value_snapshots(self, accountName=None):
        if accountName is None:
            accountName = self.uns.request_from_dict(dsvca.accounts_as_dict())

        account = dsvca.account_by_name(accountName)

        equities = dsvce.equities_by_account(account.id)

        self.uns.pretty_print_items(sorted(equities, key=lambda x: x.equityType),
                                    title="Equities Snapshots")

    def print_equities(self):
        self.uns.pretty_print_items(dsvce.query_equities("").to_json(), title="Equities")
