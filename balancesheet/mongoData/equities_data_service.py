from balancesheet.mongoData.equities import Equity
from balancesheet.mongoData.valueSnapshot import ValueSnapshot
from typing import List, Dict
from balancesheet.enums import AssetType, LiabiltyType, EquityContingency, EquityTimeHorizon, EquityClass, EquityStatus



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
        return enter_equity(name,description, accountId, equityClass, equityType, equityTimeHorizon, equityStatus, equityContingency, interestRate)

def delete_equity(account_id:str, equity_name:str):
    equity = equity_by_account_and_name(account_id, equity_name)

    equity.delete()


def equities_as_dict() -> Dict[int, str]:
    accounts = query_equities('')
    return {i + 1: accounts[i].account_name for i in range(0, len(accounts))}

def query_equities(query) -> List[Equity]:
    if query == "":
        return Equity.objects().order_by('name')
    else:
        return Equity.obects(__raw__=query).order_by('name')




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

    equity = Equity.objects(id=equity.id)
    updated = False
    for snap in equity.snapshots:
        if (snap.year == year) and (snap.month == month):
            snap.value = value
            updated = True

    if not updated:
        equity.snapshots.append(valueSnapshot)

    equity.save()

    return valueSnapshot




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