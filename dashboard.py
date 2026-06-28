import streamlit as st

def dashboard():

    st.title("🏛 COSMAS Dashboard")

    st.success(
        f"Welcome {st.session_state.username} 👋"
    )

    st.metric(
        "Saved Calculations",
        "0"
    )

    st.metric(
        "Current CGPA",
        "0.00"
    )

    st.info(
        "Use the sidebar to navigate."
    )