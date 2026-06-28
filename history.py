import streamlit as st
import pandas as pd
from database import cursor

def show():

    st.title("📊 Calculation History")

    cursor.execute(
        """
        SELECT gpa,cgpa,date
        FROM history
        WHERE username=?
        ORDER BY date DESC
        """,
        (st.session_state.username,)
    )

    rows = cursor.fetchall()

    if rows:

        df = pd.DataFrame(
            rows,
            columns=[
                "Semester GPA",
                "CGPA",
                "Date"
            ]
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        csv = df.to_csv(index=False).encode()

        st.download_button(
            "📥 Download History",
            csv,
            "history.csv",
            "text/csv"
        )

    else:

        st.info("No saved calculations yet.")