import streamlit as st
import pandas as pd
from utils import get_pie_chart, get_pm_pie, get_bar_chart, get_barh_chart, get_group_bar_chart, get_line_chart, get_multi_line_chart

def apply_filters(df, year_filter, target_filter):
    # Check if a specific year or target filter has been selected
    year_filter_selected = year_filter != ["All"]
    target_filter_selected = target_filter != "All"

    # Create the filtered DataFrame if a filter has been selected
    if year_filter_selected and not target_filter_selected:
        filtered_df = df[df['Order Date'].dt.year.isin(year_filter)]
    elif target_filter_selected and not year_filter_selected:
        filtered_df = df[df['Gain/Loss'] == target_filter]
    elif year_filter_selected and target_filter_selected:
        filtered_df = df[df['Order Date'].dt.year.isin(year_filter) & (df['Gain/Loss'] == target_filter)]
    else:
        filtered_df = df

    return filtered_df

def sales_tab(df, year_filter, target_filter):
    filtered_df = apply_filters(df, year_filter, target_filter)

    # Create the first row with 2 charts
    col1, col2 = st.columns(2)
    with col1:
        st.header('Sales by Category')
        fig1 = get_pie_chart(df=filtered_df, groupby_col='Category', values_col='Sales')
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.header('Sales by Segment')
        fig2 = get_pie_chart(df=filtered_df, groupby_col='Segment', values_col='Sales')
        st.plotly_chart(fig2, use_container_width=True)

    col3 = st.columns(1)[0]
    with col3:
        st.header('Sales by Region')
        fig3 = get_bar_chart(df=filtered_df, x_column='Region', y_column='Sales', color_column='Region',
                    title='', xaxis_title='Region', yaxis_title='Sales')
        st.plotly_chart(fig3, use_container_width=True)

    col4 = st.columns(1)[0]
    with col4:
        st.header('Sales by Sub-Category')
        fig4 = get_group_bar_chart(df=filtered_df, x_column='Sub-Category', y_column='Sales', color_column='Category',
                    title='', xaxis_title='Sub-Category', yaxis_title='Sales')
        st.plotly_chart(fig4, use_container_width=True)
    
    col5 = st.columns(1)[0]
    with col5:
        st.header('Sales by Order Date')
        fig5 = get_line_chart(df=filtered_df, x='Order Date', y='Sales', title='')
        st.plotly_chart(fig5, use_container_width=True)

def profit_tab(df, year_filter, target_filter):
    filtered_df = apply_filters(df, year_filter, target_filter)

    # Create the first row with 2 charts
    col6, col7 = st.columns(2)
    with col6:
        st.header('Profit by Category')
        fig6 = get_pie_chart(df=filtered_df, groupby_col='Category', values_col='Profit')
        st.plotly_chart(fig6, use_container_width=True)

    with col7:
        st.header('Profit by Segment')
        fig7 = get_pie_chart(df=filtered_df, groupby_col='Segment', values_col='Profit')
        st.plotly_chart(fig7, use_container_width=True)

    col8 = st.columns(1)[0]
    with col8:
        st.header('Profit by Region')
        fig8 = get_bar_chart(df=filtered_df, x_column='Region', y_column='Profit', color_column='Region',
                    title='', xaxis_title='Region', yaxis_title='Profit')
        st.plotly_chart(fig8, use_container_width=True)

    col9 = st.columns(1)[0]
    with col9:
        st.header('Profit by Sub-Category')
        fig9 = get_group_bar_chart(df=filtered_df, x_column='Sub-Category', y_column='Profit', color_column='Category',
                    title='', xaxis_title='Sub-Category', yaxis_title='Profit')
        st.plotly_chart(fig9, use_container_width=True)
    
    col10 = st.columns(1)[0]
    with col10:
        st.header('Profit by Order Date')
        fig10 = get_line_chart(df=filtered_df, x='Order Date', y='Profit', title='')
        st.plotly_chart(fig10, use_container_width=True)

def comparison_tab(df, year_filter, target_filter):
    filtered_df = apply_filters(df, year_filter, target_filter)

    col11 = st.columns(1)[0]
    with col11:
        st.header('Sales and Profit by Category')
        fig11 = get_barh_chart(df=filtered_df, x='Category', y=['Sales', 'Profit'], 
                        barmode='group', title='')
        st.plotly_chart(fig11, use_container_width=True)
    
    col12 = st.columns(1)[0]
    with col12:
        st.header('Sales and Profit by Sub-Category')
        fig12 = get_barh_chart(df=filtered_df, x='Sub-Category', y=['Sales', 'Profit'], 
                        barmode='group', title='')
        st.plotly_chart(fig12, use_container_width=True)

    col13 = st.columns(1)[0]
    with col13:
        st.header('Sales and Profit by Region')
        fig13 = get_barh_chart(df=filtered_df, x='Region', y=['Sales', 'Profit'], 
                        barmode='group', title='')
        st.plotly_chart(fig13, use_container_width=True)
    
    col14 = st.columns(1)[0]
    with col14:
        st.header('Sales and Profit by Order Date')
        fig14 = get_multi_line_chart(df=filtered_df, x='Order Date', y1='Sales', y2='Profit', title='')
        st.plotly_chart(fig14, use_container_width=True)

def app():
    st.title('Analyzing Customer Preferences and Effective Marketing with a Data-Driven Approach to Retail Strategies')

    # Get DataFrame
    df = pd.read_csv('dataset/superstore_clean_latest.csv', parse_dates=['Order Date'])
    df_trans = pd.read_csv('dataset/superstore_transform.csv')

    # Define filters
    year_filter_options = list(df['Order Date'].dt.year.unique())
    year_filter_options.insert(0, 'All')
    year_filter = st.sidebar.multiselect('Select Year', year_filter_options, default='All')

    target_filter_options = list(df['Gain/Loss'].unique())
    target_filter_options.insert(0, 'All')
    target_filter = st.sidebar.selectbox('Select Target', target_filter_options, index=0)

    # Define tabs
    tabs = {
        'Sales': sales_tab,
        'Profit': profit_tab,
        'Comparison': comparison_tab
    }
    selected_tab = st.sidebar.selectbox("Select a tab", list(tabs.keys()))

    if selected_tab == 'Sales':
        tabs[selected_tab](df, year_filter, target_filter)
    elif selected_tab == 'Profit':
        tabs[selected_tab](df, year_filter, target_filter)
    elif selected_tab == 'Comparison':
        tabs[selected_tab](df, year_filter, target_filter)
        
if __name__ == '__main__':
    app()