import streamlit as st
from multiapp import MultiApp
from apps import Prediction, Alldiagrams # import your app modules here

app = MultiApp()



# Add all your application here
app.add_app("All Diagrams", Alldiagrams.app)
app.add_app("Prediction", Prediction.app)

# The main app
app.run()
