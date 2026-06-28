import streamlit as st
import pandas as pd
import database


def show():

    st.title("👤 My Profile")

    st.subheader("Account Information")

    st.write(f"**Username:** {st.session_state.username}")

    # Get user details
    database.cursor.execute(
        """
        SELECT email
        FROM users
        WHERE username=?
        """,
        (st.session_state.username,)
    )

    user = database.cursor.fetchone()

    if user:
        st.write(f"**Email:** {user[0]}")

    st.divider()

    # Statistics
    database.cursor.execute(
        """
        SELECT COUNT(*), MAX(cgpa), AVG(cgpa)
        FROM history
        WHERE username=?
        """,
        (st.session_state.username,)
    )

    stats = database.cursor.fetchone()

    total_results = stats[0] if stats[0] else 0
    highest_cgpa = stats[1] if stats[1] else 0.0
    average_cgpa = stats[2] if stats[2] else 0.0

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Saved Results",
        total_results
    )

    col2.metric(
        "Highest CGPA",
        f"{highest_cgpa:.2f}"
    )

    col3.metric(
        "Average CGPA",
        f"{average_cgpa:.2f}"
    )

    st.divider()

    st.subheader("📜 Recent Results")

    database.cursor.execute(
        """
        SELECT cgpa, date
        FROM history
        WHERE username=?
        ORDER BY date DESC
        LIMIT 5
        """,
        (st.session_state.username,)
    )

    rows = database.cursor.fetchall()

    if rows:

        df = pd.DataFrame(
            rows,
            columns=[
                "CGPA",
                "Date"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True
        )

    else:

        st.info("No calculations saved yet.")

    st.divider()

    if st.button("🚪 Logout"):

        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
