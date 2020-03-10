from ledgerkeeper.mongoData.account import Account
import ledgerkeeper.mongoData.ledger_data_service as dsvcl
import ledgerkeeper.mongoData.account_data_service as dsvca
import balancesheet.mongoData.equities_data_service as dsvce
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import datetime
from dateutil.relativedelta import relativedelta
from datetime import date, timedelta
from typing import List

# print(plt.style.available)
mpl.style.use(['ggplot'])  # optional: for ggplot-like style

from ledgerkeeper.enums import TransactionTypes


def _print_df(df: pd.DataFrame):
    with pd.option_context('display.max_rows', 100, 'display.max_columns', 2000, 'display.width', 250):
        print(df)

def plot_history_by_category(recent_months:int, print_data=False, account: Account = None):
    if account is None:
        ledger_items = dsvcl.query_ledger("", True)
    else:
        ledger_items = dsvcl.query_ledger()

    data = pd.DataFrame(ledger_items)
    start_date = datetime.datetime.now() - relativedelta(months=+recent_months)
    spent = dsvcl.expense_history(start_date, end_date=datetime.datetime.today())
    spent = spent[(spent['spend_category'] != "_NA")]


    if print_data:
        _print_df(spent)


    grouped_spent = spent.groupby([pd.Grouper(freq='M'), pd.Grouper('spend_category')]).sum()

    if print_data:
        _print_df(grouped_spent)

    pivot = pd.pivot_table(grouped_spent, values=['debit'], index=['date_stamp'], columns=['spend_category']).fillna(0)

    if print_data:
        _print_df(pivot)

    income = data[(data['transaction_category'] == TransactionTypes.APPLY_INCOME.name)
                & (data['date_stamp'] >= datetime.datetime.now() - relativedelta(months=+recent_months))]\
                [['date_stamp', 'credit']]
    income.index = income['date_stamp']
    grouped_income = income.groupby([pd.Grouper(freq='M')]).sum()

    if print_data:
        _print_df(grouped_income)

    ax = plt.subplot()
    pivot.plot(kind="area", alpha=.15, figsize=(15, 10), ax=ax)
    grouped_income.plot(kind="line", alpha=.85, ax=ax, color=['yellow'])

    plt.title("Spend History by Category")
    plt.xlabel("Month")
    plt.ylabel("Amount")
    plt.show()

def plot_projected_finance(relevant_past_mo: int, relevant_future_months: int, current_balance: float, one_time_transactions = None):
    sdate = date.today() - relativedelta(months=+relevant_past_mo)
    edate = date.today() + relativedelta(months=+relevant_future_months)

    delta = edate - sdate  # as timedelta

    expenses = dsvcl.expense_history(sdate, edate)
    grouped_expenses = expenses[(expenses['spend_category'] != "_NA")].groupby(pd.Grouper(freq='D')).sum()

    # _print_df(grouped_expenses)
    grouped_income = dsvcl.income_history(sdate, edate).groupby(pd.Grouper(freq='D')).sum()
    _print_df(grouped_income)

    dates = []
    for i in range(delta.days + 1):
        day = sdate + timedelta(days=i)
        dates.append(day)

    dates = pd.DataFrame({'date_stamp': (pd.Timestamp(date) for date in dates)})
    # _print_df(dates)

    dates_with_history = pd.merge(dates, grouped_expenses, how="left", left_on="date_stamp", right_on="date_stamp")
    dates_with_history = pd.merge(dates_with_history, grouped_income, how="left",  left_on="date_stamp", right_on="date_stamp")
    dates_with_history = dates_with_history.fillna(0)


    dates_with_history['day'] = dates_with_history.date_stamp.dt.day
    _print_df(dates_with_history)

    grouped_avg_by_day = dates_with_history.groupby(by=dates_with_history.day).mean()
    _print_df(grouped_avg_by_day)

    index_of_today = dates_with_history.index[dates_with_history.date_stamp == datetime.datetime.today().strftime('%Y-%m-%d')].tolist()[0]

    # Project Future Transactions
    if one_time_transactions is None:
        one_time_transactions = {}
    last_period_total = current_balance
    for ii in range(index_of_today, len(dates_with_history)):
        day_of_month = dates_with_history.iloc[ii]['date_stamp'].day
        avg_debit = grouped_avg_by_day.iloc[day_of_month - 1]['debit']
        avg_credit = grouped_avg_by_day.iloc[day_of_month - 1]['credit']

        last_period_total = last_period_total - avg_debit + avg_credit + one_time_transactions.get(dates_with_history.iloc[ii]['date_stamp'], 0)
        dates_with_history.at[ii, 'EoD'] = last_period_total

    # Enter old transactions
    next_period_total = current_balance
    for ii in range(index_of_today, 0, -1):
        dates_with_history.at[ii, 'EoD'] = next_period_total
        next_period_total = next_period_total - dates_with_history.iloc[ii]['credit'] + dates_with_history.iloc[ii][
            'debit']

    #Trendline
    trend = dates_with_history[dates_with_history.day == 15][['date_stamp', 'EoD']]


    dates_with_history['debit'] = -dates_with_history.debit
    dates_with_history = dates_with_history[['date_stamp', 'debit', 'credit', 'EoD']].fillna(0)

    _print_df(dates_with_history)

    # instantiate fig and ax object
    fig, axes = plt.subplots(nrows=1, ncols=1, sharex=True, figsize=(15, 5))

    ax1 = plot_datetime(dates_with_history, axes, xaxis='date_stamp', ylabel="Amount")
    ax2 = plot_datetime(trend, axes, xaxis='date_stamp', ylabel='Trend', linestyle='--')
    show_plot(axes, fig, "Projected Financial Outlook")


def plot_assets_liabilities_worth_over_time(relevant_months: int, print_data=False, accountIds: List[str] = None):
    balance_over_time = dsvce.balance_over_time_data(relevant_months, accountIds)

    if print_data:
        with pd.option_context('display.max_rows', 500, 'display.max_columns', 2000, 'display.width', 250):
            print(balance_over_time)

    balance_over_time_grouped = balance_over_time.groupby([pd.Grouper('BOM'), pd.Grouper('class')]).sum()

    if print_data:
        with pd.option_context('display.max_rows', 500, 'display.max_columns', 2000, 'display.width', 250):
            print(balance_over_time_grouped)

    pivot = pd.pivot_table(balance_over_time_grouped, values=['value'], index=['BOM'], columns=['class']).fillna(0)
    pivot.sort_values(by=['BOM'], inplace=True)
    flattened = pd.DataFrame(pivot.to_records())
    flattened.columns = [hdr.replace("('value', \'", "").replace("\')", "") \
                     for hdr in flattened.columns]
    flattened['NETWORTH'] = flattened['ASSET'] - flattened['LIABILITY']

    if print_data:
        with pd.option_context('display.max_rows', 500, 'display.max_columns', 2000, 'display.width', 250):
            print(flattened)

    # instantiate fig and ax object
    fig, axes = plt.subplots(nrows=1, ncols=1, sharex=True, figsize=(15, 5))

    ax1 = plot_datetime(flattened, axes, xaxis='BOM', ylabel="ASSET")
    # ax2 = plot_datetime(flattened, axes, xaxis='BOM', ylabel='LIABILITY', linestyle='--')
    show_plot(axes, fig, "Assets, Liabilities, Net Worth over time")


def show_plot(axes, fig,
              title="[Title]",
              saveloc=None):
    axes.set_title(title, fontsize=14)
    plt.show()

    # savefig if
    if saveloc:
        fig.savefig(saveloc)

def plot_datetime(df,
                  axes,
                  xaxis=None,
                  highlight=True,
                  weekend=5,
                  ylabel="Number of Visits",
                  facecolor='green',
                  alpha_span=0.2,
                  linestyle='-'):
    """
    Draw a plot of a dataframe
    df(pandas) = pandas dataframe
    highlight(bool) = to highlight or not
    title(string) = title of plot
    saveloc(string) = where to save file
    """

    _print_df(df)

    if xaxis is None:
        df['_tmp_'] = df.index
        xaxis = '_tmp_'

    # draw all columns of dataframe
    for v in df.columns.tolist():
        if v != xaxis:
            df.plot(x=xaxis, y=v, kind='line', ax=axes, linestyle=linestyle)

    # if highlight:
    #     # find weekend indeces
    #     weekend_indices = find_weekend_indices(df.index, weekend=5)
    #     # highlight weekends
    #     highlight_datetimes(weekend_indices, axes, df, facecolor)

    # set y label
    axes.set_ylabel(ylabel)
    axes.legend()
    # plt.tight_layout()

    # add xaxis gridlines
    axes.xaxis.grid(b=True, which='major', color='black', linestyle='--', alpha=1)
        
    return axes

if __name__ == "__main__":
    import mongo_setup
    mongo_setup.global_init()

    # plot_history_by_category(10, True)
    # plot_projected_finance(3, 3, 10000)
    plot_assets_liabilities_worth_over_time(relevant_months=5, print_data=True, accountIds=["5e625935df67fa15ba672615"])