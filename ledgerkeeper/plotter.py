import mongoData.ledger_data_service as dsvcl
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import datetime
from dateutil.relativedelta import relativedelta

# print(plt.style.available)
mpl.style.use(['ggplot'])  # optional: for ggplot-like style

from enums import TransactionTypes


def _print_df(df: pd.DataFrame):
    with pd.option_context('display.max_rows', 100, 'display.max_columns', 2000, 'display.width', 250):
        print(df)

def plot_history_by_category(recent_months:int, print_data=False):

    ledger_items = dsvcl.query_ledger("", True)
    data = pd.DataFrame(ledger_items)
    spent = data[(data['transaction_category'] == TransactionTypes.RECORD_EXPENSE.name)
                & (data['spend_category'] != "_NA")
                & (data['date_stamp'] >= datetime.datetime.now() - relativedelta(months=+recent_months))]
    spent.index = spent['date_stamp']

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


# def plot_datetime(df, title="Yelp Businesses Checkins",
#                   highlight=True,
#                   weekend=5,
#                   ylabel="Number of Visits",
#                   saveloc=None,
#                   facecolor='green',
#                   alpha_span=0.2):
#     """
#     Draw a plot of a dataframe that has datetime object as its index
#     df(pandas) = pandas dataframe with datetime as indeces
#     highlight(bool) = to highlight or not
#     title(string) = title of plot
#     saveloc(string) = where to save file
#     """
#
#     # instantiate fig and ax object
#     fig, axes = plt.subplots(nrows=1, ncols=1, sharex=True, figsize=(15, 5))
#
#     # draw all columns of dataframe
#     for v in df.columns.tolist():
#         axes.plot(df[v], label=v, alpha=.8)
#
#     if highlight:
#         # find weekend indeces
#         weekend_indices = find_weekend_indices(df.index, weekend=5)
#         # highlight weekends
#         highlight_datetimes(weekend_indices, axes, df, facecolor)
#
#     # set title and y label
#     axes.set_title(title, fontsize=12)
#     axes.set_ylabel(ylabel)
#     axes.legend()
#     plt.tight_layout()
#
#     # add xaxis gridlines
#     axes.xaxis.grid(b=True, which='major', color='black', linestyle='--', alpha=1)
#
#     # savefig if
#     if saveloc:
#         fig.savefig(saveloc)

if __name__ == "__main__":
    import mongo_setup
    mongo_setup.global_init()

    plot_history_by_category(10, True)