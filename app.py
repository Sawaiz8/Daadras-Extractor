import streamlit as st
import streamlit_authenticator as stauth
from pages.session_creator import session_creator_page
from pages.data_ingestion import data_ingestion_page
from pages.individual_student_data_portal import individual_student_data_page
from pages.analytics_dashboard import analytics_dashboard_page
import asyncio
from utilities.mongo_db.streamlit_mongo_wrapper import get_all_session_names, get_section_names
if "first_run" not in st.session_state.keys():
    st.session_state["first_run"] = True

# Initialize session state for authentication status
if "authentication_status" not in st.session_state:
    st.session_state["authentication_status"] = None

credentials = {
    'usernames': {
        'admin': {
            'email': st.secrets['credentials']['usernames']['admin']['email'],
            'name': st.secrets['credentials']['usernames']['admin']['name'],
            'password': st.secrets['credentials']['usernames']['admin']['password']
        }
    }
}
authenticator = stauth.Authenticate(
    credentials,
    st.secrets['cookie']['name'],
    st.secrets['cookie']['key'],
    st.secrets['cookie']['expiry_days'],
    st.secrets['preauthorized']
)

def intro_page():
    st.title("Welcome to Daadras IT Assessment System")
    st.markdown("Choose a session to analyze and manage applications.")


def auth_page():
    name, st.session_state["authentication_status"], username = authenticator.login('main')
    if st.session_state["authentication_status"]:
        st.rerun()
    elif st.session_state["authentication_status"] == False:
        st.error('Username/password is incorrect')


if st.session_state["authentication_status"]:
    logout_button = st.sidebar.button("Logout")
    if logout_button:
        st.session_state["on_page"] = None
        st.session_state["authentication_status"] = None
        st.rerun()
    if "on_page" not in st.session_state.keys():
        st.session_state["on_page"] = None
        intro_page()

    header_1, header_2 = st.sidebar.columns(2)
    header_1.write("**دادرس**")
    header_2.caption("Daadras Assessment System")

    sessions = get_all_session_names()
    st.session_state["sessions"] = sessions

    if "current_page" not in st.session_state.keys():
        st.session_state["current_page"] = "Intro"

    session_selector = st.sidebar.selectbox(
        "Select Session",
        sessions,
        index=None,
        key='selection',
    )

    if session_selector:
        st.session_state["selected_session"] = session_selector
        # Fetch section names for the selected session
        section_names = get_section_names(session_selector)
        # Display section names in a dropdown
        selected_section = st.sidebar.selectbox("Select Section", section_names)
        if selected_section:
            st.session_state["selected_section"] = selected_section
            if st.sidebar.button("Access", type="primary"):
                st.session_state["show_buttons"] = True
            
            # Show buttons if they should be visible
            if st.session_state.get("show_buttons", False):
                analytics_dashboard = st.sidebar.button(label="Analytics Dashboard", use_container_width=True, key="analytics_dashboard")
                if analytics_dashboard:
                    st.session_state["on_page"] = "Analytics Dashboard"
                individual_student_data = st.sidebar.button("Individual Student Data", use_container_width=True, key="individual_student_data")
                if individual_student_data:
                    st.session_state["on_page"] = "Individual_Student_Data"

    st.sidebar.divider()
    st.sidebar.caption("Create Session")

    if st.sidebar.button(label="Session Management"):
        st.session_state["on_page"] = "Create Session"
    if st.sidebar.button(label="Data Ingestion"):
        st.session_state["on_page"] = "Data Ingestion"

    if st.session_state["on_page"] == "Create Session":
        session_creator_page()
    elif st.session_state["on_page"] == "Data Ingestion":
        data_ingestion_page()
    elif st.session_state["on_page"] == "Individual_Student_Data":
        individual_student_data_page()
    elif st.session_state["on_page"] == "Analytics Dashboard":
        analytics_dashboard_page()

else:
    auth_page()

