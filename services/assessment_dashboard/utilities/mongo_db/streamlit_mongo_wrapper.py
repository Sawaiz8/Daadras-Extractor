import streamlit as st
from main.database import mongo_store
import asyncio

@st.cache_data(ttl=300)
def get_all_session_names():
    return asyncio.run(mongo_store.get_all_session_names())

@st.cache_data(ttl=300)
def get_section_names(session_name):
    return asyncio.run(mongo_store.get_section_names(session_name))

@st.cache_data(ttl=300)
def get_students_by_session_and_section(session_name, section_name):
    return asyncio.run(mongo_store.get_students_by_session_and_section(session_name, section_name))
