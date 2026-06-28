import streamlit as st
import pandas as pd
import io
import database


def calculator():

    st.title("🎓 CGPA Calculator")

    # --------------------------
    # Session State
    # --------------------------
    if "courses" not in st.session_state:
        st.session_state.courses = []

    st.subheader("Previous Record")

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

    grades = {
        "A":5,
        "B":4,
        "C":3,
        "D":2,
        "E":1,
        "F":0
    }

    with st.form("course_form", clear_on_submit=True):

        code = st.text_input(
            "Course Code"
        )

        col1,col2 = st.columns(2)

        with col1:

            cu = st.number_input(
                "Credit Unit",
                min_value=1,
                max_value=6
            )

        with col2:

            grade = st.selectbox(
                "Grade",
                list(grades.keys())
            )

        submit = st.form_submit_button(
            "Add Course"
        )

        if submit:

            code = code.upper().strip()

            if code == "":

                st.error(
                    "Enter course code."
                )

            elif any(
                c["Course"] == code
                for c in st.session_state.courses
            ):

                st.warning(
                    "Course already exists."
                )

            else:

                st.session_state.courses.append({

                    "Course":code,

                    "Credit Units":cu,

                    "Grade":grade,

                    "GP":grades[grade],

                    "Quality Points":cu*grades[grade]

                })

                st.success(
                    f"{code} added."
                )

    # --------------------------
    # Result
    # --------------------------

    if st.session_state.courses:

        df = pd.DataFrame(
            st.session_state.courses
        )

        total_cu = df["Credit Units"].sum()

        total_qp = df["Quality Points"].sum()

        semester_gpa = total_qp / total_cu

        grand_cu = prev_cu + total
