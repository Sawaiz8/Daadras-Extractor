import asyncio
import streamlit as st
from controllers.session_section import save_attendance_pdf, format_student_name
from utilities.mongo_db.streamlit_mongo_wrapper import get_students_by_session_and_section
from main.database import mongo_store

def individual_student_data_page():
    session_selector = st.session_state["selected_session"]
    selected_section = st.session_state["selected_section"]

    students = get_students_by_session_and_section(session_selector, selected_section)
    output_filename = f"{session_selector}_{selected_section}_attendance.pdf"
    output_file_path = f"data/attendance_sheets/{output_filename}"
    save_attendance_pdf(student_dict=students, program_name=session_selector, section=selected_section, output_file_path=output_file_path)
    with open(output_file_path, "rb") as pdf_file:
        st.download_button(
            label="Download Attendance PDF",
            data=pdf_file,
            file_name=output_filename,
            mime="application/pdf"
        )

    student_names = [format_student_name(student) for student in students]
    selected_student = st.selectbox("Select Student", student_names)

    # Find the selected student details
    selected_student_details = next((student for student in students if format_student_name(student) == selected_student), None)

    if selected_student_details:
        st.markdown("---")
        show_update_form = st.session_state.get("show_update_form", False)
        if not show_update_form:
            # Place the "Update Data" button beside the subheader
            col1, col2 = st.columns([3, 1])
            with col1:
                st.subheader("Student Details")
            with col2:
                if st.button("Update Data", key="update_data_button"):
                    st.session_state["show_update_form"] = True
                    st.rerun()

            # Use columns for basic info
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Name:** {selected_student}")
                st.markdown(f"**Age:** {selected_student_details.get('age', 'N/A')}")
                st.markdown(f"**Gender:** {selected_student_details.get('gender', 'N/A')}")
            with col2:
                st.markdown(f"**Email:** {selected_student_details.get('email', 'N/A')}")
                st.markdown(f"**Contact Number:** {selected_student_details.get('contact_number', 'N/A')}")
                st.markdown(f"**City:** {selected_student_details.get('city', 'N/A')}")
                st.markdown(f"**Address:** {selected_student_details.get('address', 'N/A')}")

            # Pre-Test Data
            with st.expander("Pre-Test Data", expanded=True):
                pre_test_data = selected_student_details.get('pre_test_data', {})
                st.markdown("**Written Exam Scores:**")
                if pre_test_data.get('written_exam_scores'):
                    st.table([
                        {"Subject": key.replace('_', ' ').title(), "Score": value}
                        for key, value in pre_test_data.get('written_exam_scores', {}).items()
                    ])
                else:
                    st.write("No written exam scores available.")

                st.markdown("**Viva:**")
                if pre_test_data.get('viva'):
                    st.table([
                        {"Topic": key.replace('_', ' ').title(), "Score": value}
                        for key, value in pre_test_data.get('viva', {}).items()
                    ])
                else:
                    st.write("No viva data available.")

                st.markdown("**Practical Exam Reports:**")
                if pre_test_data.get('practical_exam_reports'):
                    st.table([
                        {"Task": key.replace('_', ' ').title(), "Score": value}
                        for key, value in pre_test_data.get('practical_exam_reports', {}).items()
                    ])
                else:
                    st.write("No practical exam reports available.")

            # Post-Test Data
            with st.expander("Post-Test Data", expanded=True):
                post_test_data = selected_student_details.get('post_test_data', {})
                st.markdown("**Written Exam Scores:**")
                if post_test_data.get('written_exam_scores'):
                    st.table([
                        {"Subject": key.replace('_', ' ').title(), "Score": value}
                        for key, value in post_test_data.get('written_exam_scores', {}).items()
                    ])
                else:
                    st.write("No written exam scores available.")

                st.markdown("**Viva:**")
                if post_test_data.get('viva'):
                    st.table([
                        {"Topic": key.replace('_', ' ').title(), "Score": value}
                        for key, value in post_test_data.get('viva', {}).items()
                    ])
                else:
                    st.write("No viva data available.")

                st.markdown("**Practical Exam Reports:**")
                if post_test_data.get('practical_exam_reports'):
                    st.table([
                        {"Task": key.replace('_', ' ').title(), "Score": value}
                        for key, value in post_test_data.get('practical_exam_reports', {}).items()
                    ])
                else:
                    st.write("No practical exam reports available.")

        else:
            st.subheader("Update Student Information")
            with st.form("edit_student_form"):
                col1, col2 = st.columns(2)
                with col1:
                    first_name = st.text_input("First Name", value=selected_student_details.get('first_name', ''))
                    middle_name = st.text_input("Middle Name", value=selected_student_details.get('middle_name', ''))
                    last_name = st.text_input("Last Name", value=selected_student_details.get('last_name', ''))
                    age = st.number_input("Age", value=selected_student_details.get('age', 0), min_value=0)
                    gender = st.selectbox("Gender", options=["Male", "Female", "Other"], index=["Male", "Female", "Other"].index(selected_student_details.get('gender', 'Male')))
                with col2:
                    email = st.text_input("Email", value=selected_student_details.get('email', ''))
                    contact_number = st.text_input("Contact Number", value=selected_student_details.get('contact_number', ''))
                    city = st.text_input("City", value=selected_student_details.get('city', ''))
                    address = st.text_area("Address", value=selected_student_details.get('address', ''))

                # Editable fields for pre-test and post-test data
                with st.expander("Edit Pre-Test Data", expanded=False):
                    pre_test_data = selected_student_details.get('pre_test_data', {})
                    written_exam_scores = pre_test_data.get('written_exam_scores', {}).copy()
                    viva = pre_test_data.get('viva', {}).copy()
                    practical_exam_reports = pre_test_data.get('practical_exam_reports', {}).copy()

                    for key in written_exam_scores:
                        # Convert value to float before passing to number_input
                        value = written_exam_scores.get(key, 0)
                        if isinstance(value, str):
                            try:
                                value = float(value)
                            except ValueError:
                                value = 0
                        written_exam_scores[key] = st.number_input(f"Pre-Test {key.replace('_', ' ').title()}", value=value)

                    for key in viva:
                        viva[key] = st.text_input(f"Pre-Test Viva {key.replace('_', ' ').title()}", value=viva.get(key, ''))

                    for key in practical_exam_reports:
                        practical_exam_reports[key] = st.text_input(f"Pre-Test Practical {key.replace('_', ' ').title()}", value=practical_exam_reports.get(key, ''))

                with st.expander("Edit Post-Test Data", expanded=False):
                    post_test_data = selected_student_details.get('post_test_data', {})
                    post_written_exam_scores = post_test_data.get('written_exam_scores', {}).copy()
                    post_viva = post_test_data.get('viva', {}).copy()
                    post_practical_exam_reports = post_test_data.get('practical_exam_reports', {}).copy()

                    for key in post_written_exam_scores:
                        # Convert value to float before passing to number_input
                        value = post_written_exam_scores.get(key, 0)
                        if isinstance(value, str):
                            try:
                                value = float(value)
                            except ValueError:
                                value = 0
                        post_written_exam_scores[key] = st.number_input(f"Post-Test {key.replace('_', ' ').title()}", value=value)

                    for key in post_viva:
                        post_viva[key] = st.text_input(f"Post-Test Viva {key.replace('_', ' ').title()}", value=post_viva.get(key, ''))

                    for key in post_practical_exam_reports:
                        post_practical_exam_reports[key] = st.text_input(f"Post-Test Practical {key.replace('_', ' ').title()}", value=post_practical_exam_reports.get(key, ''))

                submitted = st.form_submit_button("Update Student Info")

            if submitted:
                with st.spinner("Updating student information..."):
                    update_fields = {}
                    if first_name != selected_student_details.get('first_name', ''):
                        update_fields['first_name'] = first_name
                    if middle_name != selected_student_details.get('middle_name', ''):
                        update_fields['middle_name'] = middle_name
                    if last_name != selected_student_details.get('last_name', ''):
                        update_fields['last_name'] = last_name
                    if age != selected_student_details.get('age', 0):
                        update_fields['age'] = age
                    if gender != selected_student_details.get('gender', 'Male'):
                        update_fields['gender'] = gender
                    if email != selected_student_details.get('email', ''):
                        update_fields['email'] = email
                    if contact_number != selected_student_details.get('contact_number', ''):
                        update_fields['contact_number'] = contact_number
                    if city != selected_student_details.get('city', ''):
                        update_fields['city'] = city
                    if address != selected_student_details.get('address', ''):
                        update_fields['address'] = address

                    # Update pre-test and post-test data
                    update_fields['pre_test_data'] = {
                        'written_exam_scores': written_exam_scores,
                        'viva': viva,
                        'practical_exam_reports': practical_exam_reports
                    }
                    update_fields['post_test_data'] = {
                        'written_exam_scores': post_written_exam_scores,
                        'viva': post_viva,
                        'practical_exam_reports': post_practical_exam_reports
                    }

                    if update_fields:
                        asyncio.run(mongo_store.update_student_fields(session_selector, selected_section, selected_student_details['student_id'], update_fields))
                        st.success("Student information updated successfully!")
                        st.session_state["show_update_form"] = False
                        st.rerun()
                    else:
                        st.info("No changes detected.")

    else:
        st.error("Student details not found.")
