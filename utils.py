import time
import streamlit as st
import pandas as pd

@st.cache_data
def create_dataframe() -> pd.DataFrame:
    """Merges treasury par yield csv files in data/"""

    df_1 = pd.read_csv("data/yield-curve-rates-2001-2010.csv"
                       ,parse_dates=['Date']
                       ,date_format='%m/%d/%y')
    df_2 = pd.read_csv("data/yield-curve-rates-2011-2020.csv"
                       ,parse_dates=['Date']
                       ,date_format='%m/%d/%y')

    df = pd.concat([df_1, df_2], ignore_index=True)

    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

    df.sort_values(by=['Date'], inplace=True)

    df.set_index('Date', inplace=True)

    return df

def data_message():

    message = """
            The treasury data was source from the [Treasury Interest Rates Par Yield Curve](https://home.treasury.gov/interest-rates-data-csv-archive)

            """
    
    for word in message.split(" "):
        yield word + " "
        time.sleep(0.10)
                              

@st.cache_data
def generate_abs_diffs(df: pd.DataFrame, fill_method: str = 'ffill')-> pd.DataFrame:
    """Given input dataframe of par rates generate diff table in basis points
    
        fill_method: accepts either 'ffill' or 'bfill'

        prefer data to be sorted oldest as first row, and use forward fill to fill down nulls.
    """

    # sort dataframe in descending, apply either forward or backward fill and diff

    df.sort_index(inplace=True)

    df_diff = df.ffill().diff()

    df_diff = df_diff.mul(100)

    return df_diff
