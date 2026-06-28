import streamlit as st
import pandas as pd
import io
import database


def show():

    st.title("📊 Calculation History")

    database.cursor.execute(
        """
        SELECT id, gpa, cgpa, total_cu, total_qp, date
        FROM history
        WHERE username=?
        ORDER BY date DESC
        """,
        (st.session_state.username,)
    )

    rows = database.cursor.fetchall()

    if not rows:
        st.info("No saved calculations yet.")
        return

    df = pd.DataFrame(
        rows,
        columns=[
            "ID",
            "Semester GPA",
            "CGPA",
            "Credit Units",
            "Quality Points",
            "Date"
        ]
    )

    # Search
    search = st.text_input(
        "🔍 Search by Date"
    )

    if search:
        df = df[df["Date"].astype(str).str.contains(search)]

    st.dataframe(
        df,
        use_container_width=True
    )

    st.divider()

    # Delete Record
    record = st.selectbox(
        "Select Record to Delete",
        df["ID"]
    )

    if st.button("🗑 Delete Record"):

        database.cursor.execute(
            "DELETE FROM history WHERE id=?",
            (int(record),)
        )

        database.conn.commit()

        st.success("Record deleted successfully.")

        st.rerun()

    st.divider()

    # Download CSV
    csv = io.BytesIO()

    df.to_csv(
        csv,
        index=False
    )

    st.download_button(
        "📥 Download History",
        csv.getvalue(),
        "cgpa_history.csv",
        "text/csv"
    )
