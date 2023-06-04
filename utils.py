import streamlit as st
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from datetime import datetime
from dateutil.relativedelta import relativedelta

# functions
def bold(text):
    """This function return text with bold

    Args:
        text (str): normal text to bold

    Returns:
        str: A bold text
    """
    return f"**{text}**"

def calculate_age(dob):
    """
    Calculate age based on date of birth.

    Args:
        dob (str): Date of birth in format "YYYY-MM-DD"

    Returns:
        int: Age in years
    """
    today = datetime.now().date()
    dob = datetime.strptime(dob, "%Y-%m-%d").date()
    age = relativedelta(today, dob).years
    return age

def get_bar_chart(df, x, y, barmode=None, color=None, category_orders=None, labels=None, title=None):
    """This method visualizes the data into a bar chart.

    Args:
        df (Pandas DataFrame): Preprocessed data from raw sources
        x (str): Usually a column name in DataFrame, to set x-axis
        y (str): Usually a column name in DataFrame, to set y-axis
        barmode (str): Choose barmode from 'group', 'stack' or 'relative'. Defaults to 'relative'
        color (str): Usually a column name in the DataFrame, to assign colors to categories
        category_orders (dict): To set order of categorical values in axes, legends or facets
        labels (dict): To override/rename axis titles, legend entries or hovers
        title (str): The title of figure

    Returns:
        Plotly Bar Chart: A bar chart.
    """
    
    df[x] = df[x].astype(str)

    df = df.groupby([x, color], as_index=False).agg({y:'count'})

    fig = px.bar(df, x=x, y=y,
                     barmode=barmode, color=color, 
                     category_orders=category_orders, 
                     labels=labels,
                     title=title)
    # fig.update_layout(showlegend=True, width=600, height=400)
    fig.update_layout(showlegend=True)
    fig.update_traces(marker_line_width=0, opacity=0.95)
    fig.update_xaxes(title_text=" ")

    return fig

def get_pie_chart(df, values, names, category_orders=None, labels=None, title=None):
    """This method visualizes the data into a pie chart.

    Args:
        df (Pandas DataFrame): Preprocessed data from raw sources
        values (str): Usually a column name in DataFrame, to get values
        names (str): Usually a column name in DataFrame, to get names
        category_orders (dict): To set order of categorical values in axes, legends or facets
        labels (dict): To override/rename axis titles, legend entries or hovers
        title (str): The title of figure

    Returns:
        Plotly Pie Chart: A pie chart.
    """
    
    df[values] = df[values].astype(str)

    df_count = df[names].value_counts().reset_index()
    df_count.columns = [names, values]

    fig = px.pie(df_count, values=values, names=names,
                     category_orders=category_orders, 
                     labels=labels,
                     title=title)
    # fig.update_layout(showlegend=True, width=600, height=400)
    fig.update_layout(showlegend=True)
    fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig

def get_histogram(df, column, bins_range, bin_width, x_label, y_label, title=None):
    """This method visualizes the data into a histogram.

    Args:
        df (Pandas DataFrame): Preprocessed data from raw sources
        column (str): Usually a column name in DataFrame, to set column to be used for the histogram
        bins_range (tuple): A tuple containing the range of the bins (start, end)
        bin_width (int): The width of the bins
        x_label (str): The label for the x-axis. Defaults to 'x'
        y_label (str): The label for the y-axis. Defaults to 'y'
        title (str): The title of the figure. Defaults to None

    Returns:
        Plotly Histogram: A histogram.
    """
    # create the bins
    counts, bins = np.histogram(df[column], bins=range(*bins_range, bin_width))
    bins = 0.5 * (bins[:-1] + bins[1:])

    fig = px.bar(x=bins, y=counts, labels={x_label:x_label, y_label:y_label}, title=title)

    # Update the axis labels
    fig.update_xaxes(title_text=x_label)
    fig.update_yaxes(title_text=y_label)
    # fig.update_layout(showlegend=True, width=600, height=400)
    fig.update_layout(showlegend=True)

    return fig
 
def get_features(df):
    """This method visualizes the data into a barchat on features importance.

    Args:
        df (Pandas DataFrame): Preprocessed data from raw sources

    Returns:
        Plotly Bar Chart: A barchart.
    """
    corr_with_target = df.corr()['target'].sort_values(ascending=False)

    fig = px.bar(
        x=corr_with_target.index, 
        y=corr_with_target.values, 
        labels={'x': 'Features', 'y': 'Coefficient'},
        color=corr_with_target.index,
        title='Correlation with Target'
    )
    fig.update_xaxes(showticklabels=False, title='')
    
    return fig