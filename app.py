import streamlit as st
import database
import auth
import dashboard
import calculator
import history
import profile
import settings

# Initialize database
database.conn.commit()

# Page configuration
st.set_page_config(
    page_title="Cosmas CGPA Calculator",
    page_icon="🎓",
    layout="wide"
)

# Session State
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# ===========================
# LOGIN / SIGN UP PAGE
# ===========================

if not st.session_state.logged_in:

    st.title("🏛️ COSMAS AT SUG TOP SEAT")
    st.caption("Support • Pray • Canvass")

    st.markdown("---")

    tab1, tab2 = st.tabs(["🔑 Login", "📝 Create Account"])

    # ---------------- LOGIN ----------------

    with tab1:

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            if auth.login(username, password):

                st.session_state.logged_in = True
                st.session_state.username = username

                st.success("Login Successful")

                st.rerun()

            else:

                st.error("Invalid Username or Password")

    # ---------------- SIGNUP ----------------

    with tab2:

        new_username = st.text_input(
            "Choose Username"
        )

        email = st.text_input(
            "Email Address"
        )

        new_password = st.text_input(
            "Choose Password",
            type="password"
        )

        if st.button("Create Account"):

            if auth.signup(
                new_username,
                email,
                new_password
            ):

                st.success(
                    "Account Created Successfully!"
                )

            else:

                st.error(
                    "Username or Email already exists."
                )

# ===========================
# DASHBOARD
# ===========================

else:

    with st.sidebar:

        st.image(
            "cosmas_banner.jpg",
            use_container_width=True
        )

        st.success(
            f"Welcome\n\n{st.session_state.username}"
        )

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

        st.markdown("---")

        if st.button("🚪 Logout"):

            st.session_state.logged_in = False

            st.session_state.username = ""

            st.rerun()

    # ---------------- Pages ----------------

    if page == "🏠 Dashboard":

        dashboard.dashboard()

    elif page == "🎓 CGPA Calculator":

        calculator.calculator()

    elif page == "📊 History":

        history.show()

    elif page == "👤 Profile":

        profile.show()

    elif page == "⚙️ Settings":

        settings.show()
