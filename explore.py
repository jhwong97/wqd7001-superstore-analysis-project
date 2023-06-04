import streamlit as st
import pandas as pd
from utils import get_histogram, get_pie_chart, get_bar_chart, get_features

def distribution_tab(df, sex_filter, target_filter):
    # Check if a specific sex or target filter has been selected
    sex_filter_selected = sex_filter != "All"
    target_filter_selected = target_filter != "All"

    # Create the filtered dataframe if a filter has been selected
    if sex_filter_selected and not target_filter_selected:
        filtered_df = df[df['sex'] == sex_filter]
    elif target_filter_selected and not sex_filter_selected:
        filtered_df = df[df['target'] == target_filter]
    elif sex_filter_selected and target_filter_selected:
        filtered_df = df[(df['sex'] == sex_filter) & (df['target'] == target_filter)]
    else:
        filtered_df = df

    # Create the first row with 2 charts
    col1, col2 = st.columns(2)

    with col1:
        st.header('Age Distribution')
        fig1 = get_histogram(df=filtered_df, column='age', bins_range=(20, 80), bin_width=10, x_label='age', y_label='count')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.header('Gender Distribution')
        fig2 = get_pie_chart(df=filtered_df, values='age', names='sex', labels={'age': 'Count'})
        st.plotly_chart(fig2, use_container_width=True)

def feature_target__tab(df, sex_filter, target_filter):
    # Check if a specific sex or target filter has been selected
    sex_filter_selected = sex_filter != "All"
    target_filter_selected = target_filter != "All"

    # Create the filtered dataframe if a filter has been selected
    if sex_filter_selected and not target_filter_selected:
        filtered_df = df[df['sex'] == sex_filter]
    elif target_filter_selected and not sex_filter_selected:
        filtered_df = df[df['target'] == target_filter]
    elif sex_filter_selected and target_filter_selected:
        filtered_df = df[(df['sex'] == sex_filter) & (df['target'] == target_filter)]
    else:
        filtered_df = df
    
    col3, col4 = st.columns(2)
    with col3:
        st.header('Gender by Heart Disease')
        fig3 = get_bar_chart(filtered_df, 'sex', 'age', color='target', barmode='group',
                    category_orders={'sex': ['Female', 'Male']}, 
                    labels={'sex': 'Gender', 'age': 'Count', 'target': 'Target'})
        st.plotly_chart(fig3, use_container_width=True)
    
    with col4:
        st.header('Chest Pain Type by Heart Disease')
        fig4 = get_bar_chart(filtered_df, 'chest_pain_type', 'age', color='target', barmode='group',
                    labels={'chest_pain_type': 'Chest Pain Type', 'age': 'Count', 'target': 'Target'})
        st.plotly_chart(fig4, use_container_width=True)
    
    col5, col6 = st.columns(2)
    with col5:
        st.header('Number of Major Vessels by Heart Disease')
        fig5 = get_bar_chart(filtered_df, 'number_of_major_vessels', 'age', color='target', barmode='group',
                    category_orders={'number_of_major_vessels': [0, 1, 2, 3]}, 
                    labels={'number_of_major_vessels': 'Number of Major Vessels', 'age': 'Count', 'target': 'Target'})
        st.plotly_chart(fig5, use_container_width=True)
    
    with col6:
        st.header('Thalassemia Disorder by Heart Disease')
        fig6 = get_bar_chart(filtered_df, 'thalassemia_disorder', 'age', color='target',
                    category_orders={'thalassemia_disorder': ['Normal Blood Flow', 'Fixed Defect', 'Reversible Defect']}, 
                    labels={'thalassemia_disorder': 'Thalassemia Disorder', 'age': 'Count', 'target': 'Target'})
        st.plotly_chart(fig6, use_container_width=True)

def features_tab(df):
    st.header('Features Correlation')
    fig6 = get_features(df)
    st.plotly_chart(fig6, use_container_width=True)

def app():
    st.title('Heart Diseases Analytics Dashboard')

    # Get DataFrame
    df = pd.read_csv('dataset/Heart_clean.csv')
    df_trans = pd.read_csv('dataset/Heart_transform.csv')

    # Define filters
    sex_filter_options = list(df['sex'].unique())
    sex_filter_options.insert(0, 'All')
    sex_filter = st.sidebar.selectbox('Select Gender', sex_filter_options, index=0)

    target_filter_options = list(df['target'].unique())
    target_filter_options.insert(0, 'All')
    target_filter = st.sidebar.selectbox('Select Target', target_filter_options, index=0)

   # Define tabs
    tabs = {
        'Distribution': distribution_tab,
        'Features by Target': feature_target__tab,
        'Features': features_tab
    }
    selected_tab = st.sidebar.selectbox("Select a tab", list(tabs.keys()))

    if selected_tab == 'Distribution':
        tabs[selected_tab](df, sex_filter, target_filter)
    elif selected_tab == 'Features by Target':
        tabs[selected_tab](df, sex_filter, target_filter)
    elif selected_tab == 'Features':
        tabs[selected_tab](df_trans)
        
if __name__ == '__main__':
    app()