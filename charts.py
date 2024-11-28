import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def rate_line_chart(df: pd.DataFrame, y: str = "10 Yr"):
    """Given rates dataframe, will plot single rate vs date.

       Returns plotly figure.
    """
    title = f"{y} Treasury Par Rate"

    fig = px.line(df, y=y, title=title,)
    fig.update_traces(textposition="bottom right")
    
    return fig

def histogram_chart(df: pd.DataFrame, x: str = "10 Yr"):
    """Given rates diff dataframe, will return histogram distribution.

       Returns plotly figure.
    """

    fig = px.histogram(df, x=x)

    fig.add_vline(x=-5, line_width=3, line_dash="dash", line_color="red")
    
    return fig

def cumulative_dist_chart(df: pd.DataFrame, x: str = "10 Yr"):
    """Given rates diff dataframe, will return cumulative distribution.

       Returns plotly figure.
    """

    fig = px.ecdf(df[x], markers=True, lines=True, marginal="histogram")
    
    return fig