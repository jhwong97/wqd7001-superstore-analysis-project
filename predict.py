import streamlit as st
import pandas as pd
import xgboost as xgb
import joblib
from utils import bold

def app():
    # Create a Streamlit app
    st.title("Product Prediction (Profit/Not Profit)")

    # Load the trained model
    model = joblib.load('trained_model/xgbclassifier.joblib')

    seg_option =  {0:'Consumer', 1:'Corporate', 2:'Home Office'}
    stat_option =  {0:'Alabama', 1:'Arizona', 2:'Arkansas', 3:'California', 4:'Colorado', 5:'Connecticut', 6:'Delaware',
                7:'District of Columbia', 8:'Florida', 9:'Georgia', 10:'Idaho', 11:'Illinois', 12:'Indiana', 13:'Iowa',
                14:'Kansas', 15:'Kentucky', 16:'Louisiana', 17:'Maine', 18:'Maryland', 19:'Massachusetts', 20:'Michigan', 
                21:'Minnesota', 22:'Mississippi', 23:'Missouri', 24:'Montana', 25:'Nebraska', 26:'Nevada', 27:'New Hampshire', 
                28:'New Jersey', 29:'New Mexico', 30:'New York', 31:'North Carolina', 32:'North Dakota', 33:'Ohio', 34:'Oklahoma', 
                35:'Oregon', 36:'Pennsylvania', 37:'Rhode Island', 38:'South Carolina', 39:'South Dakota', 40:'Tennessee', 41:'Texas', 
                42:'Utah', 43:'Vermont', 44:'Virginia', 45:'Washington', 46:'West Virginia', 47:'Wisconsin', 48:'Wyoming'}
    reg_option =  {0:'Central', 1:'East', 2:'South', 3:'West'}
    cat_option =  {0:'Furniture', 1:'Office Supplies', 2:'Technology'}
    scat_option =  {0:'Accessories', 1:'Appliances', 2:'Art', 3:'Binders', 4:'Bookcases', 5:'Chairs', 6:'Copiers', 
                        7:'Envelopes', 8:'Fasteners', 9:'Furnishings', 10:'Labels', 11:'Machines', 12:'Paper', 13:'Phones', 
                        14:'Storage', 15:'Supplies', 16:'Tables'}

    # Create a form for user input
    with st.form(key='profit_form'):
        # Input fields
        segment = st.selectbox(bold('Segment'), options=list(seg_option.keys()), format_func=lambda x: seg_option[x])
        state = st.selectbox(bold('State'), options=list(stat_option.keys()), format_func=lambda x: stat_option[x])
        region = st.selectbox(bold('Region'), options=list(reg_option.keys()), format_func=lambda x: reg_option[x])
        category = st.selectbox(bold('Category'), options=list(cat_option.keys()), format_func=lambda x: cat_option[x])
        sub_category = st.selectbox(bold('Sub-Category'), options=list(scat_option.keys()), format_func=lambda x: scat_option[x])
        sales = st.number_input(bold('Sales'), value=0.0)
        quantity = st.number_input(bold('Quantity'), value=0)
        discount = st.slider(bold('Discount'), min_value=0.0, max_value=1.0, value=0.0, step=0.05)

        # Submit button
        submit_button = st.form_submit_button(label='Predict')

    # Perform prediction when form is submitted
    if submit_button:
        # Prepare input features for prediction
        X = pd.DataFrame({
            'Segment': [segment],
            'State': [state],
            'Region': [region],
            'Category': [category],
            'Sub-Category': [sub_category],
            'Sales': [sales],
            'Quantity': [quantity],
            'Discount': [discount]
        })

        # Make prediction
        y_pred = model.predict(X)

        # Display prediction result
        if y_pred[0] == 1:
            st.write(bold("Prediction: Profitable"))
        else:
            st.write(bold("Prediction: Not Profitable"))


if __name__ == '__main__':
    app()