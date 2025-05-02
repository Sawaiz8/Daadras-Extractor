import streamlit as st
from main.database import mongo_store
import asyncio
from utilities.utils import create_written_exam_template, create_viva_audio_template, create_practical_exam_template

def data_ingestion_page():
    st.title("Data Ingestion for Session")
    session_names = asyncio.run(mongo_store.get_all_session_names())
    selected_session = st.selectbox("Choose a session", session_names, key="ingestion_selector")
    if selected_session is not None:
        section_names = asyncio.run(mongo_store.get_section_names(selected_session))
        selected_section = st.selectbox("Choose a section", section_names, key="section_selector")
        if selected_section is not None:
            st.subheader("Written Exam Scores")
            students = asyncio.run(mongo_store.get_students_by_session_and_section(selected_session, selected_section))
            written_exam_template = create_written_exam_template(students, selected_section)
            st.download_button("Download Written Exam Scores Template", written_exam_template, "written_exam_template.zip", "application/zip")
            written_exam_zip = st.file_uploader("Upload Written Exam Scores (ZIP)", type="zip", key="written_exam_zip")

            st.subheader("Viva Audio Files")
            viva_audio_template = create_viva_audio_template(students, selected_section)
            st.download_button("Download Viva Audio Files Template", viva_audio_template, "viva_audio_template.zip", "application/zip")
            viva_audio_zip = st.file_uploader("Upload Viva Audio Files (ZIP)", type="zip", key="viva_audio_zip")
            
            st.subheader("Practical Exam Report Notes")
            practical_exam_template = create_practical_exam_template(students, selected_section)
            st.download_button("Download Practical Exam Report Notes Template", practical_exam_template, "practical_exam_template.zip", "application/zip")
            practical_exam_zip = st.file_uploader("Upload Practical Exam Report Notes (ZIP)", type="zip", key="practical_exam_zip")

            if st.button("Ingest Data"):
                st.success("Data ingestion confirmed!")
                # Here you would typically process and store the data
