import streamlit as st
from explore import app as explore_app
from predict import app as predict_app

def main():
    st.set_page_config(page_title="Streamlit", layout="wide")

    st.sidebar.title('Navigation')
    menu = ['Explore', 'Predict']
    choice = st.sidebar.selectbox('Select a page', menu)

    if choice == 'Explore':
        explore_app()
    elif choice == 'Predict':
        predict_app()

if __name__ == '__main__':
    main()