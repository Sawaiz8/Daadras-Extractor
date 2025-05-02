import pandas as pd
import streamlit as st
from time import sleep
import os

def session_updater_page():
    st.title("Update Session Data")
    selected_project = st.selectbox("Choose a project", st.session_state["project_sessions"], key="update_selector")
    if selected_project is not None:
        st.subheader("Chess")
        chess_link = st.text_input("Link to CHESS Sheet")
        st.subheader("IT")
        it_link = st.text_input("Link to IT Sheet")
        st.subheader("SEL")
        sel_link = st.text_input("Link to SEL Sheet")
        with st.popover("Update"):
            st.error("Are you sure?")
            update_button = st.button("Confirm")


        
