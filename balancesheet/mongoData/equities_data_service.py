from balancesheet.mongoData.equities import Equity
from balancesheet.mongoData.valueSnapshot import ValueSnapshot
from typing import List, Dict
from balancesheet.enums import AssetType, LiabiltyType, EquityContingency, EquityTimeHorizon, EquityClass, EquityStatus
from mongoengine.queryset.visitor import Q
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta


def enter_equity(name:str,
                 description:str,
                 accountId: str,
                 equityClass: EquityClass,
                 equityType: [AssetType, LiabiltyType],
                 equityTimeHorizon : EquityTimeHorizon,
                 equityStatus:EquityStatus,
                 equityContingency:EquityContingency,
                 interestRate: float = 0.0) -> Equity:

    equity = Equity()
    equity.name = name
    equity.description = description
    equity.account_id = accountId
    equity.equityClass = equityClass.name
    equity.equityType = equityType.name
    equity.equityTimeHorizon = equityTimeHorizon.name
    equity.equityStatus = equityStatus.name
    equity.equityContingency = equityContingency.name
    equity.interestRate = interestRate

    equity.save()

    return equity

def enter_if_not_exists(name:str,
                        description:str,
                        accountId:str,
                        equityClass: EquityClass,
                        equityType: [AssetType, LiabiltyType],
                        equityTimeHorizon : EquityTimeHorizon,
                        equityStatus:EquityStatus,
                        equityContingency:EquityContingency,
                        interestRate: float = 0.0) -> Equity:

    existing = Equity.objects(name=name)

    if len(existing) > 0:
        return None
    else:
        return enter_equity(name, description, accountId, equityClass, equityType, equityTimeHorizon, equityStatus,
                            equityContingency, interestRate)

def delete_equity(account_id:str, equity_name:str):
    equity = equity_by_account_and_name(account_id, equity_name)
    if equity is None:
        raise Exception(f"Account Id: [{account_id}], equity_name {equity_name} not found.")
    equity.delete()


def equities_as_dict(accountIds:List[str] = None) -> Dict[int, str]:

    equities = query_equities('', raw_return=False, accountIds=accountIds)
    return {i + 1: equities[i].name for i in range(0, len(equities))}

def query_equities(query, raw_return=True, accountIds:List[str] = None) -> List[Equity]:
    if query == "":
        equities = Equity.objects()
    else:
        equities = Equity.objects().filter(__raw__=query)

    if accountIds is not None:
        account_query = Q(account_id__in=accountIds).to_query(Equity)
        equities = equities.filter(__raw__=account_query)

    equities = equities.order_by('name')

    if raw_return:
        return equities.as_pymongo()
    else:
        ret_equities = []
        for l in equities.order_by('name'):
            ret_equities.append(l)

        return ret_equities

def query_values_over_time_by_accounts(query, raw_return=True, accountIds:List[str] = None):
    equities = query_equities("", raw_return=False, accountIds=accountIds)

    values =[]
    for equity in equities:
        for value in equity.snapshots:
            values.append({"accountId":equity.account_id, "name": equity.name, "class": equity.equityClass,
                           "year": value.year, "month": value.month, "value": value.value})

    return values

    if accountIds is not None:
        account_query = Q(account_id__in=accountIds).to_query(Equity)
        equities = equities.filter(__raw__=account_query)



def equity_by_account_and_name(account_id: str, equity_name: str) -> Equity:
    return Equity.objects()\
                .filter(account_id=account_id)\
                .filter(name=equity_name)\
                .first()

def equities_by_account(account_id: str) -> Equity:
    return Equity.objects()\
                .filter(account_id=account_id)\
                .first()

def record_value_on_equity(equity: Equity,
                           year: int,
                           month: int,
                           value: float
                            ) -> ValueSnapshot:
    valueSnapshot = ValueSnapshot()
    valueSnapshot.year = year
    valueSnapshot.month = month
    valueSnapshot.value = value

    equity = Equity.objects(id=equity.id).first()
    updated = False
    for snap in equity.snapshots:
        if (snap.year == year) and (snap.month == month):
            snap.value = value
            updated = True

    if not updated:
        equity.snapshots.append(valueSnapshot)

    equity.save()

    return valueSnapshot

def balance_over_time_data(relevant_months: int, accountIds: List[str] = None):
    if accountIds is None:
        values = query_values_over_time_by_accounts("", True)
    else:
        values = query_values_over_time_by_accounts("", True, accountIds)

    data = pd.DataFrame(values)

    start_date = datetime.datetime.now() - relativedelta(months=+relevant_months)
    month = start_date.month
    year = start_date.year
    timed_data = data[(12 * data.year + data.month) >= 12 * year + month]
    timed_data['BOM'] = pd.to_datetime(dict(year=timed_data.year, month=timed_data.month, day=1))

    return timed_data


def balance_sheet_over_time(relevant_months: int, accountIds: List[str] = None):
    timed_data = balance_over_time_data(relevant_months=relevant_months, accountIds=accountIds)

    pivot = pd.pivot_table(timed_data, values=['value'], index=['accountId', 'class', 'name'], columns=['BOM']).fillna(0)
    pivot.sort_index( axis=1, ascending=False, inplace=True)
    pivot.sort_values(by=['accountId', 'class', 'name'], inplace=True)

    # with pd.option_context('display.max_rows', 500, 'display.max_columns', 2000, 'display.width', 250):
    #     print(pivot)
    return pivot

if __name__ == "__main__":
    import mongo_setup
    mongo_setup.global_init()

    name="test"
    description="test equity"
    accountId = "12345"
    equityClass=EquityClass.ASSET
    equityType=AssetType.ANNUITY
    equityTimeHorizon=EquityTimeHorizon.LONG_TERM
    equityStatus=EquityStatus.OPEN
    equityContingency=EquityContingency.FIXED
    interestRate = .01
    ret = enter_if_not_exists(name,description, accountId, equityClass, equityType, equityTimeHorizon, equityStatus, equityContingency, interestRate)

    if ret is not None:
        print("Equity added successfully")
    else:
        print("Unable to add. Equity already exists")
        
    # delete_equity(accountId, name)