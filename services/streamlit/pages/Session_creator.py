import streamlit as st
from shutil import rmtree
from time import sleep
import os
from main.database import mongo_store
import asyncio
def session_creator_page():

    st.title("Project Management")

    # Create new session
    st.header("Create a New Session")
    new_session_name = st.text_input("Session Name")
    school_name = st.text_input("School Name")
    school_location = st.text_input("School Location")
    project_start_date = st.date_input("Project Start Date (Optional)", key="start_date", value=None)
    project_end_date = st.date_input("Project End Date (Optional)", key="end_date", value=None)

    st.write("### Section Details")
    section_names = []
    section_files = []  # List to store uploaded files
    section_count = st.session_state.get("section_count", 1)

    for i in range(section_count):
        section_name = st.text_input(f"Section Name {i+1}", key=f"section_{i}")
        section_names.append(section_name)
        
        # File uploader for each section
        uploaded_file = st.file_uploader(f"Upload Excel for {section_name}", type=['xlsx', 'xls', "csv", "ods"], key=f"file_{i}")
        section_files.append(uploaded_file)

    if st.button("+ Add Section"):
        st.session_state["section_count"] = section_count + 1
        st.rerun()

    if st.button("Save Session"):
        session_data = {
            "session_name": new_session_name,
            "school_name": school_name,
            "school_location": school_location,
            "start_date": project_start_date,
            "end_date": project_end_date,
            "sections": [{"section_name": section_name} for section_name in section_names],
        }


        if new_session_name and school_name and school_location:
            asyncio.run(mongo_store.upsert_session_data(session_data))
            st.success("Session created successfully")
            st.rerun()
        else:
            st.error("Please provide a session name, school name, and school location.")

    st.header("Delete Session")
    delete_selector = st.selectbox("Choose a session", st.session_state["project_sessions"], key="delete")
    with st.popover("Delete"):
        st.error("Are you sure?")
        delete_button = st.button("Confirm")
    if delete_selector and delete_button:
        try:
            rmtree(f"./database/{delete_selector}")
            st.success("Session Deleted Successfully!")
            sleep(1.0)
            st.rerun()
        except OSError as e:
            st.error("Error deleting session!")
            st.write(e)
