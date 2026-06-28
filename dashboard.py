import streamlit as st
import pandas as pd
import database


def dashboard():

    st.title("🏛️ Dashboard")

    st.success(f"Welcome back, {st.session_state.username} 👋")

    # Get user's history
    database.cursor.execute(
        """
        SELECT gpa, cgpa, total_cu, total_qp, date
        FROM history
        WHERE username=?
        ORDER BY date DESC
        """,
        (st.session_state.username,)
    )

    rows = database.cursor.fetchall()

    if not rows:
        st.info("You haven't saved any CGPA calculations yet.")
        return

    df = pd.DataFrame(
        rows,
        columns=[
            "Semester GPA",
            "CGPA",
            "Credit Units",
            "Quality Points",
            "Date"
        ]
    )

    # Metrics
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Saved Results",
        len(df)
    )

    col2.metric(
        "Highest CGPA",
        f"{df['CGPA'].max():.2f}"
    )

    col3.metric(
        "Latest CGPA",
        f"{df.iloc[0]['CGPA']:.2f}"
    )

    st.divider()

    st.subheader("📈 CGPA Progress")

    chart_df = df.iloc[::-1][["CGPA"]]
    st.line_chart(chart_df)

    st.divider()

    st.subheader("🕒 Recent Calculations")

    st.dataframe(
        df,
        use_container_width=True
    )
