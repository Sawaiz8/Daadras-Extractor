import streamlit as st
from shutil import rmtree
from time import sleep
import os
from main.database import mongo_store
import asyncio
import pandas as pd

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
        session_data = {
            "session_name": new_session_name,
            "school_name": school_name,
            "school_location": school_location,
            "start_date": project_start_date,
            "end_date": project_end_date,
            "sections": [{"section_name": section_name} for section_name in section_names],
        }
        for section_name, uploaded_file in zip(section_names, section_files):
            if uploaded_file is not None:
                # Determine the file extension and specify the engine
                file_extension = uploaded_file.name.split('.')[-1]
                if file_extension in ['xlsx', 'ods']:
                    df = pd.read_excel(uploaded_file, engine='openpyxl')
                elif file_extension == 'xls':
                    df = pd.read_excel(uploaded_file, engine='xlrd')
                elif file_extension == 'csv':
                    df = pd.read_csv(uploaded_file)
                else:
                    st.error("Unsupported file format")
                    continue

                # Iterate over each row in the DataFrame
                for _, row in df.iterrows():
                    student_data = {
                        "id": row.get("ID"),
                        "first_name": row.get("first_name"),
                        "middle_name": row.get("middle_name", None),
                        "last_name": row.get("last_name"),
                        "age": row.get("age"),
                        "gender": row.get("gender"),
                        "session_name": new_session_name,
                        "section_name": section_name,
                        "classes_attended": None,
                        "email": None,
                        "contact_number": None,
                        "city": None,
                        "address": None,
                        "pre_test_data": {
                            "written_exam_scores": {
                                "written_ai_section_score": None,
                                "written_env_score": None,
                                "written_internet_score": None,
                                "written_canva_score": None,
                                "written_programming_score": None,
                                "written_hardware_software_score": None,
                                "other_new_section_score_aggregated": None,
                                "total_student_marks": None,
                                "total_marks_of_exam": None,
                                "start_time_exam": None,
                                "end_time_exam": None
                            },
                            "viva": {
                                "transcript": None,
                                "analysis": None,
                                "duration": None
                            },
                            "practical_exam_reports": {
                                "report": None,
                                "analysis": None,
                                "start_time_exam": None,
                                "end_time_exam": None,
                            }
                        },
                        "post_test_data": {
                             "written_exam_scores": {
                                "written_ai_section_score": None,
                                "written_env_score": None,
                                "written_internet_score": None,
                                "written_canva_score": None,
                                "written_programming_score": None,
                                "written_hardware_software_score": None,
                                "other_new_section_score_aggregated": None,
                                "total_student_marks": None,
                                "total_marks_of_exam": None,
                                "start_time_exam": None,
                                "end_time_exam": None
                            },
                            "viva": {
                                "transcript": None,
                                "analysis": None,
                                "duration": None
                            },
                            "practical_exam_reports": {
                                "report": None,
                                "analysis": None,
                                "start_time_exam": None,
                                "end_time_exam": None,
                            }
                       }
                    }
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
            rmtree(f"./database/{delete_selector}")
            st.success("Session Deleted Successfully!")
            sleep(1.0)
            st.rerun()
        except OSError as e:
            st.error("Error deleting session!")
            st.write(e)
