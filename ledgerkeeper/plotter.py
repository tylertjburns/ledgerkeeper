import mongoData.ledger_data_service as dsvcl
import json
import pandas as pd
import matplotlib as plt

def plot_history_by_category():
    items_json = dsvcl.query_ledger("").to_json()
    print(items_json)
    data = pd.io.json.json_normalize(json.loads(items_json))

    for column in data.columns:
        print (column)
    data['date_stamp.$date'] = pd.to_datetime(data['date_stamp.$date'], format='%m/%d/%y %I:%M%p')
    with pd.option_context('display.max_rows', None, 'display.max_columns', 2000, 'display.width', 250):
        print(data)


    grouped_data = data.groupby(pd.Grouper(freq='M')).sum()

    with pd.option_context('display.max_rows', None, 'display.max_columns', 2000, 'display.width', 250):
        print(grouped_data)
    plt.plot(grouped_data)


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

    plot_history_by_category()