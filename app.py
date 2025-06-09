import streamlit as st

st.set_page_config(
    page_title="Komorebi Investments",
    page_icon="📊", 
    layout="wide"
)

# Redirection automatique vers Business Models
st.switch_page("pages/Business_Models.py")