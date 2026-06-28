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

if st.session_state.logged_in:

    with st.sidebar:
        st.image("cosmas_banner.jpg", use_container_width=True)
        st.success(f"👋 {st.session_state.user[1]}")

        page = st.radio(
            "Navigation",
            [
                "🏠 Dashboard",
                "🎓 CGPA Calculator",
                "📊 History",
                "👤 Profile",
                "⚙️ Settings"
            ]
        )

        if st.button("Logout"):
            auth.logout()
            st.rerun()

    if page == "🏠 Dashboard":
        st.title("Welcome Back 👋")

        c1, c2, c3 = st.columns(3)

        c1.metric("Calculations", 0)
        c2.metric("Saved Courses", 0)
        c3.metric("Current CGPA", "0.00")

        st.info("Start a new CGPA calculation from the sidebar.")

    elif page == "🎓 CGPA Calculator":
        # Put your current calculator code here
        pass

    elif page == "📊 History":
        st.title("Calculation History")
        st.info("No saved calculations yet.")

    elif page == "👤 Profile":
        st.title("My Profile")
        st.write("Username:", st.session_state.user[1])
        st.write("Email:", st.session_state.user[2])

    elif page == "⚙️ Settings":
        st.title("Settings")
        st.write("More features coming soon.")
