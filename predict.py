import streamlit as st
import pandas as pd
import joblib
from datetime import datetime
from dateutil.relativedelta import relativedelta
from utils import bold, calculate_age

def app():
    # Create a Streamlit app
    st.title("Heart Disease Prediction")

    # Calculate the minimum and maximum DOB based on years
    min_year = 1900
    max_year = datetime.now().year

    # Input for date of birth
    dob = st.date_input("Date of Birth", min_value=datetime(min_year, 1, 1), max_value=datetime(max_year, 12, 31))

    # dict and list for field names
    field_names = {
                'sex': 'Sex',
                'cp': 'Chest Pain Type',
                'trestbps': 'Resting Blood Pressure (mm Hg)',
                'chol': 'Serum Cholesterol (mg/dl)',
                'fbs': 'Fasting Blood Sugar > 120 mg/dl',
                'restecg': 'Resting ECG Results',
                'thalach': 'Maximum Heart Rate Achieved (bpm)',
                'exang': 'Exercise Induced Angina',
                'oldpeak': 'ST Depression Induced by Exercise',
                'slope': 'Slope of the Peak Exercise ST Segment',
                'ca': 'Number of Major Vessels (0-3) Colored by Fluoroscopy',
                'thal': 'Thalassemia'
                }

    field_names_list = list(field_names.values())

    # styles
    field_names_list_bold = [bold(text) for text in field_names_list]

    # options
    sex_options = {0: 'Female', 1: 'Male'}
    cp_options = {0: 'Typical Angina (TA)', 1: 'Atypical Angina (ATA)', 2: 'Non-Anginal Pain (NAP)', 3: 'Asymptomatic (ASY)'}
    fbs_options = {0: 'No', 1: 'Yes'}
    exang_options = {0: 'No', 1: 'Yes'}
    thal_options = {0: 'Normal', 1: 'Fixed Defect', 2: 'Reversable Defect'}

    # laod trained model
    heart_model = joblib.load('trained_model/decision_tree_model_demo.joblib')
    # print(heart_model)

    # Create form submission
    if dob is not None:
        age = calculate_age(str(dob))
        st.write("Current Age:", age)

        # Create a form for user input
        with st.form(key='heart_form'):
            # Input for other features
            sex = st.selectbox(field_names_list_bold[0], options=list(sex_options.keys()), format_func=lambda x: sex_options[x])
            cp = st.selectbox(field_names_list_bold[1], options=list(cp_options.keys()), format_func=lambda x: cp_options[x])
            trestbps = st.slider(field_names_list_bold[2], min_value=80, max_value=200, value=120)
            chol = st.number_input(field_names_list_bold[3], min_value=100, max_value=600, value=200)
            fbs = st.selectbox(field_names_list_bold[4], options=list(fbs_options.keys()), format_func=lambda x: fbs_options[x])
            restecg = st.selectbox(field_names_list_bold[5], options=[0, 1, 2], index=0)
            thalach = st.slider(field_names_list_bold[6], min_value=60, max_value=220, value=114)
            exang = st.selectbox(field_names_list_bold[7], options=list(exang_options.keys()), format_func=lambda x: exang_options[x])
            oldpeak = st.slider(field_names_list_bold[8], min_value=0.0, max_value=6.0, value=2.0, step=0.1)
            slope = st.selectbox(field_names_list_bold[9], options=[0, 1, 2], index=0)
            ca = st.slider(field_names_list_bold[10], min_value=0, max_value=3, value=1)
            thal = st.selectbox(field_names_list_bold[11], options=list(thal_options.keys()), format_func=lambda x: thal_options[x])

            # Submit button
            submit_button = st.form_submit_button(label='Predict')

        # Perform prediction when form is submitted
        if submit_button:
            # Prepare input features for prediction
            X = pd.DataFrame({
                'age': [age],
                'sex': [sex],
                'cp': [cp],
                'trestbps': [trestbps],
                'chol': [chol],
                'fbs': [fbs],
                'restecg': [restecg],
                'thalach': [thalach],
                'exang': [exang],
                'oldpeak': [oldpeak],
                'slope': [slope],
                'ca': [ca],
                'thal': [thal]
            })

            # Make prediction
            y_pred = heart_model.predict(X)

            # Display prediction result
            if y_pred[0] == 1:
                st.write("Prediction: Detected - User has heart disease")
            else:
                st.write("Prediction: Not Detected - User does not have heart disease")

if __name__ == '__main__':
    app()