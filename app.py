import streamlit as st
import database
import auth
import dashboard
import calculator
import history
import profile
import settings

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------
st.set_page_config(
    page_title="Cosmas CGPA Calculator",
    page_icon="🎓",
    layout="wide"
)

# -------------------------------
# LOAD CSS
# -------------------------------
def load_css():
    try:
        with open("style.css") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )
    except FileNotFoundError:
        pass

load_css()

# -------------------------------
# INITIALIZE DATABASE
# -------------------------------
database.conn.commit()

# -------------------------------
# SESSION STATE
# -------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# -------------------------------
# LOGIN / SIGN UP PAGE
# -------------------------------
if not st.session_state.logged_in:

    st.title("🏛️ COSMAS AT SUG TOP SEAT")
    st.caption("Support • Pray • Canvass")

    try:
        st.image("Cosmas_banner.png", use_container_width=True)
    except:
        st.warning("Banner image not found.")

    login_tab, signup_tab = st.tabs(
        ["🔐 Login", "📝 Create Account"]
    )

    # ---------------- LOGIN ----------------

    with login_tab:

        username = st.text_input("Username")
        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            if auth.login(username, password):

                st.session_state.logged_in = True
                st.session_state.username = username

                st.success("Login successful!")

                st.rerun()

            else:

                st.error("Invalid username or password.")

    # ---------------- SIGN UP ----------------

    with signup_tab:

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
                    "Account created successfully!"
                )

            else:

                st.error(
                    "Username or Email already exists."
                )

# -------------------------------
# MAIN APP
# -------------------------------
else:

    with st.sidebar:

        try:
            st.image(
                "Cosmas_banner.png",
                use_container_width=True
            )
        except:
            pass

        st.markdown(
            f"### 👋 Welcome\n**{st.session_state.username}**"
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

        st.divider()

        if st.button("🚪 Logout"):

            st.session_state.logged_in = False
            st.session_state.username = ""

            if "courses" in st.session_state:
                del st.session_state["courses"]

            st.rerun()

    # ---------------- PAGE ROUTING ----------------

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
