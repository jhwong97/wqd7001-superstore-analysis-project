import streamlit as st
import plotly.express as px
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from datetime import datetime

# functions
def bold(text):
    """This function return text with bold

    Args:
        text (str): normal text to bold

    Returns:
        str: A bold text
    """
    return f"**{text}**"

def get_bar_chart(df, x_column, y_column, color_column=None, title=None, xaxis_title=None, yaxis_title=None):
    df_copy = df.copy()

    grouped_data = df_copy.groupby(x_column)[y_column].sum().reset_index()
    total_value = df_copy[y_column].sum()

    grouped_data['Percentage'] = (grouped_data[y_column] / total_value) * 100

    fig = px.bar(grouped_data,
                    x=x_column,
                    y=y_column,
                    color=color_column,
                    color_discrete_sequence=px.colors.qualitative.Pastel,
                    text='Percentage')

    fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    fig.update_layout(title=title, title_font=dict(size=30),
                    xaxis_title=xaxis_title, yaxis_title=yaxis_title)

    hover_template = f"{x_column}: %{{x}}<br>{y_column}: %{{y}}<br>Percentage: %{{text}}%"
    fig.update_traces(hovertemplate=hover_template)

    return fig

def get_barh_chart(df, x, y, barmode=None, color=None, category_orders=None, labels=None, title=None):
    df_grouped = df.groupby(x)[y].sum().reset_index()
    df_grouped = df_grouped.sort_values(y, ascending=True)  # Sort in ascending order
    
    fig = px.bar(df_grouped, y=x, x=y,
                    barmode=barmode, color=color,
                    orientation='h',
                    category_orders=category_orders,
                    labels=labels,
                    title=title,
                    color_discrete_sequence=px.colors.qualitative.Pastel)
    
    fig.update_layout(showlegend=True)
    fig.update_traces(marker_line_width=0, opacity=0.95)
    fig.update_xaxes(title_text="Amount")
    fig.update_yaxes(title_text="Sub-Category")

    return fig

def get_group_bar_chart(df, x_column, y_column, color_column=None, title=None, xaxis_title=None, yaxis_title=None):
    df_copy = df.copy()

    grouped_data = df_copy.groupby(['Category', x_column])[y_column].sum().reset_index()
    total_value = df_copy[y_column].sum()

    grouped_data['Percentage'] = (grouped_data[y_column] / total_value) * 100

    grouped_data = grouped_data.sort_values(by=y_column, ascending=False)  # Sort by y_column in descending order

    fig = px.bar(grouped_data,
                    x=x_column,
                    y=y_column,
                    color=color_column,
                    color_discrete_sequence=px.colors.qualitative.Pastel,
                    text='Percentage')

    fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    fig.update_layout(title=title, title_font=dict(size=30),
                        xaxis_title=xaxis_title, yaxis_title=yaxis_title)

    hover_template = f"Category: %{grouped_data['Category']}<br>{x_column}: %{{x}}<br>{y_column}: %{{y}}<br>Percentage: %{{text}}%"
    fig.update_traces(hovertemplate=hover_template)

    return fig

def get_pie_chart(df, groupby_col, values_col, title=None):
    df_grouped = df.groupby(groupby_col)[values_col].sum().reset_index()
    df_grouped[values_col] = df_grouped[values_col].astype(float).round(2)

    fig = px.pie(df_grouped, values=values_col, names=groupby_col, title=title)
    fig.update_traces(marker=dict(colors=px.colors.qualitative.Pastel))
    fig.update_layout(showlegend=True)
    fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig

def get_pm_pie(df, values_col, names_col, title=None):
    # Calculate profit margin as a percentage
    df['Profit Margin (%)'] = (df['Profit'] / df['Sales']) * 100

    # Group the data by names_col and calculate the mean profit margin
    data = df.groupby(names_col)['Profit Margin (%)'].mean().reset_index()

    # Create the pie chart
    fig = px.pie(data, values='Profit Margin (%)', names=names_col, title=title,
                    color_discrete_sequence=px.colors.qualitative.Pastel)

    return fig

def get_line_chart(df, x, y, title=None):
    # Convert 'x' column to datetime
    df[x] = pd.to_datetime(df[x])

    # Group by 'x' and calculate the sum of 'y'
    grouped_data = df.groupby(df[x].dt.year)[y].sum().reset_index()

    # Create line chart
    fig = px.line(grouped_data, x=x, y=y, title=title, color_discrete_sequence=px.colors.qualitative.Pastel)

    # Configure x-axis
    fig.update_xaxes(
        tickmode='linear',
        nticks=4,
        tickformat='%Y'
    )

    return fig

def get_multi_line_chart(df, x, y1, y2, title=None):
    # Convert 'x' column to datetime
    df[x] = pd.to_datetime(df[x])

    # Group data by year and calculate sum of 'y1' and 'y2'
    df_grouped = df.groupby(df[x].dt.year)[[y1, y2]].sum().reset_index()

    # Create line chart
    fig = px.line(df_grouped, x=x, y=[y1, y2], title=title, color_discrete_sequence=px.colors.qualitative.Pastel)

    # Assign y-axes to respective columns
    fig.update_traces(yaxis="y1", selector=dict(name=y1))
    fig.update_traces(yaxis="y2", selector=dict(name=y2))

    # Customize the chart layout
    fig.update_layout(yaxis=dict(title=y1), yaxis2=dict(title=y2, overlaying='y', side='right'))

    # Customize the x-axis
    fig.update_layout(xaxis=dict(tickformat='%Y', dtick='M12', ticklabelmode='period'))

    return fig

# def get_histogram(df, column, bins_range, bin_width, x_label, y_label, title=None):
#     # create the bins
#     counts, bins = np.histogram(df[column], bins=range(*bins_range, bin_width))
#     bins = 0.5 * (bins[:-1] + bins[1:])

#     fig = px.bar(x=bins, y=counts, labels={x_label:x_label, y_label:y_label}, title=title)

#     # Update the axis labels
#     fig.update_xaxes(title_text=x_label)
#     fig.update_yaxes(title_text=y_label)
#     # fig.update_layout(showlegend=True, width=600, height=400)
#     fig.update_layout(showlegend=True)

#     return fig

# def get_features(df):
#     """This method visualizes the data into a barchat on features importance.

#     Args:
#         df (Pandas DataFrame): Preprocessed data from raw sources

#     Returns:
#         Plotly Bar Chart: A barchart.
#     """
#     corr_with_target = df.corr()['target'].sort_values(ascending=False)

#     fig = px.bar(
#         x=corr_with_target.index, 
#         y=corr_with_target.values, 
#         labels={'x': 'Features', 'y': 'Coefficient'},
#         color=corr_with_target.index,
#         title='Correlation with Target'
#     )
#     fig.update_xaxes(showticklabels=False, title='')
    
#     return fig