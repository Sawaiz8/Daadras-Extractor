import streamlit as st
def home():
    sessions = ["Session 1", "Session 2", "Session 3"]
    st.title("Student Information Form")
    with st.form("student_form"):
        student_id = st.number_input("Enter student id:", min_value=1, step=1)
        first_name = st.text_input("Enter student's first name:")
        mid_name = st.text_input("Enter student's mid name:")
        last_name = st.text_input("Enter student's last name:")
        age = st.number_input("Enter student's age:", min_value=1, step=1)
        date_of_birth = st.date_input("Enter student's date of birth:")
        gender = st.selectbox("Enter student's gender:", ["Male", "Female", "Other"])
        classes_attended = st.number_input("Enter student's attendance:", min_value=0, step=1)
        session_id = st.selectbox("Select session:", sessions, format_func=lambda x: f"{x[1]} (ID: {x[0]})")

        submitted = st.form_submit_button("Submit")

        if submitted:
            student_data = {
                'id': student_id,
                'first_name': first_name,
                'mid_name': mid_name,
                'last_name': last_name,
                'age': age,
                'date_of_birth': date_of_birth,
                'gender': gender,
                'classes_attended': classes_attended,
                'session_id': session_id[0]
            }
            st.success("Form submitted successfully!")
