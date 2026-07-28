import streamlit as st

def card(title, value):

    st.metric(
        label=title,
        value=value
    )
