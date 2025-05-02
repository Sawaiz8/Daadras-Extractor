import streamlit as st
import streamlit_authenticator as stauth
from pages.Home import home
from pages.Session_creator import session_creator_page
from pages.Session_updater import session_updater_page
from main.database import mongo_store
import asyncio
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

    sessions = asyncio.run(mongo_store.get_all_session_names())

    if "current_page" not in st.session_state.keys():
        st.session_state["current_page"] = "Intro"

    session_selector = st.sidebar.selectbox(
        "Select Session",
        sessions,
        index=None,
        key='selection',
    )

    accept_button = st.sidebar.button("Access", type="primary")
    if accept_button:
        st.session_state["current_page"] = "Applicant"
    st.session_state["sessions"] = sessions
    st.session_state["project_sessions"] = sessions

    st.sidebar.divider()
    st.sidebar.caption("Create Session")

    if st.sidebar.button(label="Project Management"):
        st.session_state["on_page"] = "Create Session"
    if st.sidebar.button(label="Update Data"):
        st.session_state["on_page"] = "Update Session"

    if st.session_state["on_page"] == "Create Session":
        session_creator_page()
    elif st.session_state["on_page"] == "Update Session":
        session_updater_page()

else:
    auth_page()

