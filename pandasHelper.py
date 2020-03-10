import pandas as pd

def pretty_print_dataframe(df: pd.DataFrame):
    with pd.option_context('display.max_rows', 500, 'display.max_columns', 2000, 'display.width', 250):
        print(df)
