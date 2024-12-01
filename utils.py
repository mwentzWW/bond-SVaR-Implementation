import time
import streamlit as st
import pandas as pd


@st.cache_data
def create_dataframe() -> pd.DataFrame:
    """Merges treasury par yield csv files in data/"""

    df = pd.read_csv("data/yield-curve-rates-1990-2023.csv",
                       parse_dates=['Date'], date_format='%m/%d/%y')

    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

    df.sort_values(by=['Date'], inplace=True)

    df.set_index('Date', inplace=True)

    return df


@st.cache_data
def generate_abs_diffs(df: pd.DataFrame, fill_method: str = 'ffill') -> pd.DataFrame:
    """Given input dataframe of par rates generate diff table in basis points.

        fill_method: accepts either 'ffill' or 'bfill'

        Prefer data to be sorted oldest as first row, and use forward fill to fill down nulls.

        Removes all NA rows and all NA columns.
    """

    # sort dataframe in descending, apply either forward or backward fill and diff

    df.sort_index(inplace=True)

    df_diff = df.ffill().diff()

    # remove rows where all columns are NA
    df_diff.dropna(how='all', inplace=True)

    # remove columns where all NA
    df_diff.dropna(how='all', axis='columns', inplace=True)

    df_diff = df_diff.mul(100)

    return df_diff


@st.cache_data
def generate_rel_diffs(df: pd.DataFrame, fill_method: str = 'ffill') -> pd.DataFrame:
    """Given input dataframe of par rates generate diff table percentage change.

        fill_method: accepts either 'ffill' or 'bfill'

        Prefer data to be sorted oldest as first row, and use forward fill to fill down nulls.

        Removes all NA rows and all NA columns.
    """

    # sort dataframe in descending, apply either forward or backward fill and diff

    df.sort_index(inplace=True)

    df_diff = df.ffill().pct_change()

    # remove rows where all columns are NA
    df_diff.dropna(how='all', inplace=True)

    # remove columns where all NA
    df_diff.dropna(how='all', axis='columns', inplace=True)

    return df_diff


def home_message():

    time.sleep(0.10)

    message = """
            Let's build a historical value at risk (VaR or VAR) model for treasury products 🚀
            """

    for word in message.split(" "):
        yield word + " "
        time.sleep(0.10)


def data_message():

    message = """
            The treasury data was sourced from the [Treasury Interest Rates Par Yield Curve](https://home.treasury.gov/interest-rates-data-csv-archive)
            """

    for word in message.split(" "):
        yield word + " "
        time.sleep(0.10)
