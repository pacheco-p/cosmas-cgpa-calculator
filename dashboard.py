import streamlit as st
from database import cursor

def dashboard():

    st.title("🏛️ Dashboard")

    st.success(
        f"Welcome back, {st.session_state.username} 👋"
    )

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM history
        WHERE username=?
        """,
        (st.session_state.username,)
    )

    total = cursor.fetchone()[0]

    col1, col2 = st.columns(2)

    col1.metric(
        "Saved Results",
        total
    )

    cursor.execute(
        """
        SELECT MAX(cgpa)
        FROM history
        WHERE username=?
        """,
        (st.session_state.username,)
    )

    highest = cursor.fetchone()[0]

    if highest is None:
        highest = 0

    col2.metric(
        "Highest CGPA",
        f"{highest:.2f}"
    )

    st.divider()

    st.info(
        "Use the sidebar to access your calculator, history and profile."
    )
