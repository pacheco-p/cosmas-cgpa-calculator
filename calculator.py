import streamlit as st
import pandas as pd
import io
from database import conn, cursor

grades = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1, "F": 0}


def save_history(username, gpa, cgpa):
    cursor.execute(
        """
        INSERT INTO history(username,gpa,cgpa)
        VALUES(?,?,?)
        """,
        (username, gpa, cgpa)
    )
    conn.commit()


def calculator():

    st.title("🎓 CGPA Calculator")

    if "courses" not in st.session_state:
        st.session_state.courses = []

    st.subheader("Previous Academic Record")

    prev_cu = st.number_input(
        "Previous Total Credit Units",
        min_value=0,
        value=0
    )

    prev_qp = st.number_input(
        "Previous Total Quality Points",
        min_value=0.0,
        value=0.0
    )

    st.divider()

    with st.form("course_form"):

        course = st.text_input(
            "Course Code"
        )

        col1, col2 = st.columns(2)

        with col1:

            cu = st.number_input(
                "Credit Units",
                min_value=1,
                max_value=6,
                value=3
            )

        with col2:

            grade = st.selectbox(
                "Grade",
                list(grades.keys())
            )

        add = st.form_submit_button(
            "Add Course"
        )

        if add:

            if course.strip() == "":

                st.error("Enter Course Code")

            else:

                st.session_state.courses.append({

                    "Course": course.upper(),

                    "Credit Units": cu,

                    "Grade": grade,

                    "GP": grades[grade],

                    "Quality Points": cu * grades[grade]

                })

                st.success("Course Added")

    if st.session_state.courses:

        df = pd.DataFrame(
            st.session_state.courses
        )

        st.subheader("Courses")

        st.dataframe(
            df,
            use_container_width=True
        )

        semester_cu = df["Credit Units"].sum()

        semester_qp = df["Quality Points"].sum()

        semester_gpa = semester_qp / semester_cu

        total_cu = prev_cu + semester_cu

        total_qp = prev_qp + semester_qp

        cgpa = total_qp / total_cu

        c1, c2 = st.columns(2)

        c1.metric(
            "Semester GPA",
            f"{semester_gpa:.2f}"
        )

        c2.metric(
            "CGPA",
            f"{cgpa:.2f}"
        )

        if cgpa >= 4.50:

            st.success("🏆 First Class")

        elif cgpa >= 3.50:

            st.info("🥇 Second Class Upper")

        elif cgpa >= 2.40:

            st.info("🥈 Second Class Lower")

        elif cgpa >= 1.50:

            st.warning("🎓 Third Class")

        else:

            st.error("Pass")

        if st.button("Save Result"):

            save_history(
                st.session_state.username,
                semester_gpa,
                cgpa
            )

            st.success(
                "Saved Successfully"
            )

        csv = io.BytesIO()

        df.to_csv(
            csv,
            index=False
        )

        st.download_button(

            "Download CSV",

            csv.getvalue(),

            "courses.csv",

            "text/csv"

        )

        if st.button("Clear Courses"):

            st.session_state.courses = []

            st.rerun()