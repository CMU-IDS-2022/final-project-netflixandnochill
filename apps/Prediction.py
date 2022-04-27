import streamlit as st
import numpy as np
import pandas as pd
from sklearn import datasets
import pickle

pickle_in = open("C:/Users/hamsi/OneDrive/Desktop/Interactive DS/multi-page-app-main/multi-page-app-main/apps/classifier.pkl","rb")
classifier = pickle.load(pickle_in)

def predict_content():
    prediction=classifier.predict([[country, ratings]])
    print(prediction)
    return prediction

def app():
    st.title("Prediction")
    country = st.text_input("Country","Type Here")
    ratings = st.text_input("Ratings","Type Here")
    result = ""
    if st.button("Predict"):
        result=predict_content(country, ratings)
    st.success('The output is {}'.format(result))

