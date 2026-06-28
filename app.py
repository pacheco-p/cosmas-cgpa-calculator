import streamlit as st
import database
import auth

database.init_db()

st.set_page_config(
    page_title="Cosmas CGPA Calculator",
    page_icon="🎓",
    layout="wide"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

st.title("🏛️ COSMAS AT SUG TOP SEAT")
st.caption("Support • Pray • Canvass")

if not st.session_state.logged_in:

    tab1, tab2 = st.tabs(["Login", "Create Account"])

    with tab1:

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            user = auth.login(username, password)

            if user:

                st.session_state.logged_in = True
                st.session_state.user = user

                st.success("Login Successful")

                st.rerun()

            else:

                st.error("Invalid Username or Password")

    with tab2:

        username = st.text_input("Username", key="u")

        email = st.text_input("Email")

        password = st.text_input(
            "Password",
            type="password",
            key="p"
        )

        if st.button("Create Account"):

            if auth.register(
                username,
                email,
                password
            ):

                st.success("Account Created Successfully")

            else:

                st.error("Username or Email already exists.")

else:

    st.success(
        f"Welcome {st.session_state.user[1]} 👋"
    )

    if st.button("Logout"):

        auth.logout()

        st.rerun()
