import streamlit as st
from main.database import mongo_store
import asyncio
from utilities.utils import load_file_as_dataframe
import json
import pandas as pd

with open('data/schemas/student_data_schema.json', 'r') as schema_file:
    base_student_data = json.load(schema_file)

with open('data/schemas/session_data_schema.json', 'r') as session_file:
    base_session_data = json.load(session_file)

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
        uploaded_file = st.file_uploader(f"Upload Excel for {section_name}", type=['xlsx', 'xls', 'csv', 'ods'], key=f"file_{i}")
        section_files.append(uploaded_file)

    if st.button("+ Add Section"):
        st.session_state["section_count"] = section_count + 1
        st.rerun()

    all_files_uploaded = all(f is not None for f in section_files)
    all_sections_named = all(name for name in section_names)
    can_save = new_session_name and school_name and school_location and all_sections_named and all_files_uploaded

    if st.button("Save Session", disabled=not can_save):
        session_data = base_session_data.copy()

        session_data.update({
            "session_name": new_session_name,
            "school_name": school_name,
            "school_location": school_location,
            "start_date": project_start_date,
            "end_date": project_end_date,
            "sections": [{"section_name": section_name} for section_name in section_names],
        })


        for section_name, uploaded_file in zip(section_names, section_files):
            if uploaded_file is not None:

                df = load_file_as_dataframe(uploaded_file)
                # Clean all string columns by removing empty spaces and special characters
                for col in df.select_dtypes(include=['object']).columns:
                    df[col] = df[col].str.replace(r'[^a-zA-Z0-9\s]', '', regex=True).str.strip()
                    df[col] = df[col].replace('', pd.NA)

                if df is None:
                    st.error(f"Unsupported file format for {section_name} sheet")
                    continue

                # Iterate over each row in the DataFrame
                for _, row in df.iterrows():
                    # Create a copy of the base student data
                    student_data = base_student_data.copy()

                    # Fill the student data with available information
                    student_data.update({
                        "id": row.get("ID"),
                        "first_name": row.get("first_name"),
                        "middle_name": row.get("middle_name", None),
                        "last_name": row.get("last_name"),
                        "age": row.get("age"),
                        "gender": row.get("gender"),
                        "session_name": new_session_name,
                        "section_name": section_name
                    })
                    # Save student data to the database
                    asyncio.run(mongo_store.upsert_student_data(student_data))


        if new_session_name and school_name and school_location:
            asyncio.run(mongo_store.upsert_session_data(session_data))
            st.success("Session created successfully")
            st.rerun()
        else:
            st.error("Please provide a session name, school name, and school location.")

    st.header("Delete Session")
    delete_selector = st.selectbox("Choose a session", st.session_state["sessions"], key="delete")
    with st.popover("Delete"):
        st.error("Are you sure?")
        delete_button = st.button("Confirm")
    if delete_selector and delete_button:
        try:
            asyncio.run(mongo_store.delete_session_data(delete_selector))
            st.success("Session Deleted Successfully!")
            st.rerun()
        except OSError as e:
            st.error("Error deleting session!")
            st.write(e)
