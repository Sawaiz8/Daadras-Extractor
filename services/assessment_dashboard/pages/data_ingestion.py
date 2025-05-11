import streamlit as st
import asyncio
from controllers.data_ingestion import create_score_template
from controllers.data_ingestion import process_student_data
from utilities.mongo_db.streamlit_mongo_wrapper import get_all_session_names, get_section_names, get_students_by_session_and_section

def data_ingestion_page():
    st.title("Data Ingestion for Session")
    session_names = get_all_session_names()
    selected_session = st.selectbox("Choose a session", session_names, key="ingestion_selector")
    if selected_session is not None:
        section_names = get_section_names(selected_session)
        selected_section = st.selectbox("Choose a section", section_names, key="section_selector")
        if selected_section is not None:
            st.subheader("Exam Data")
            students = get_students_by_session_and_section(selected_session, selected_section)
            score_template = create_score_template(students, selected_section)
            st.download_button("Download Exam Data Template", score_template, "exam_data_template.zip", "application/zip")
            exam_data_zip = st.file_uploader("Upload Exam Data (ZIP)", type="zip", key="exam_data_zip")

            if st.button("Ingest Data"):
                if exam_data_zip:
                    with st.spinner("Ingesting data..."):
                        process_student_data(exam_data_zip, selected_session, selected_section)
                    st.cache_data.clear()
                    st.success(f"Ingestion completed")
            
        

