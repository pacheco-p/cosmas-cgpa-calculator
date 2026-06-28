import streamlit as st
import database


def signup(username, email, password):

    username = username.strip()
    email = email.strip().lower()

    if username == "" or email == "" or password == "":
        return False

    return database.create_user(
        username,
        email,
        password
    )


def login(username, password):

    user = database.login_user(
        username,
        password
    )

    if user:
        return True

    return False


def logout():

    st.session_state.logged_in = False
    st.session_state.username = ""

    if "courses" in st.session_state:
        del st.session_state["courses"]

    st.rerun()
