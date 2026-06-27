import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Cosmas CGPA Calculator", page_icon="🎓")

# Header
st.title("🏛️ COSMAS AT SUG TOP SEAT")
st.caption("Support • Pray • Canvass")
st.divider()

# Initialize session state
if 'courses' not in st.session_state:
    st.session_state.courses = []
if 'prev_cu' not in st.session_state:
    st.session_state.prev_cu = 0
if 'prev_qp' not in st.session_state:
    st.session_state.prev_qp = 0.0

# Cumulative History Input
st.subheader("Cumulative History")
st.session_state.prev_cu = st.number_input("Previous Total Credit Units", min_value=0, step=1, value=st.session_state.prev_cu)
st.session_state.prev_qp = st.number_input("Previous Total Quality Points", min_value=0.0, step=0.1, value=st.session_state.prev_qp)

if (st.session_state.prev_cu == 0 and st.session_state.prev_qp > 0) or \
   (st.session_state.prev_cu > 0 and st.session_state.prev_qp > st.session_state.prev_cu * 5):
    st.error("Invalid cumulative data: Check your previous CU and QP.")
    st.stop()

st.divider()

# Input Section
grades = {"A": 5, "B": 4, "C": 3, "D": 2, "E": 1, "F": 0}

with st.expander("View Grade Scale"):
    st.write("A = 5 | B = 4 | C = 3 | D = 2 | E = 1 | F = 0")

with st.form("course_form", clear_on_submit=True):
    course_code = st.text_input("Course Code (e.g., CHM201)")
    col1, col2 = st.columns(2)
    with col1:
        cu = st.number_input("Credit Units", min_value=1, max_value=6, step=1)
    with col2:
        grade = st.selectbox("Grade", list(grades.keys()))
    
    submitted = st.form_submit_button("Add Course")
    
    if submitted:
        course_code = course_code.strip().upper().replace(" ", "")
        if not course_code:
            st.error("Please enter a course code.")
        elif any(c["Course"] == course_code for c in st.session_state.courses):
            st.warning("This course has already been added.")
        else:
            st.session_state.courses.append({
                "Course": course_code, 
                "Credit Units": cu, 
                "Grade": grade, 
                "GP": grades[grade],
                "Quality Points": cu * grades[grade]
            })
            st.success(f"{course_code} added!")

# Calculations & Display
if st.session_state.courses:
    df = pd.DataFrame(st.session_state.courses).sort_values("Course")
    total_qp = df["Quality Points"].sum()
    total_cu = df["Credit Units"].sum()
    
    sem_gpa = total_qp / total_cu
    grand_cu = st.session_state.prev_cu + total_cu
    grand_qp = st.session_state.prev_qp + total_qp
    cgpa = grand_qp / grand_cu if grand_cu else 0
    
    classification = "First Class" if cgpa >= 4.50 else "Second Class Upper" if cgpa >= 3.50 else "Second Class Lower" if cgpa >= 2.40 else "Third Class" if cgpa >= 1.50 else "Pass/Probation"

    # Summary Metrics
    c1, c2 = st.columns(2)
    c1.metric("Semester GPA", f"{sem_gpa:.2f}")
    c2.metric("Cumulative CGPA", f"{cgpa:.2f}")
    
    # Classification Display
    if classification == "First Class": st.success("🏆 First Class"); st.balloons()
    elif classification == "Second Class Upper": st.info("🥇 Second Class Upper")
    elif classification == "Second Class Lower": st.info("🥈 Second Class Lower")
    elif classification == "Third Class": st.warning("🎓 Third Class")
    else: st.error("⚠️ Pass/Probation")
    
    # Table Display
    st.subheader("Courses Added")
    df.index += 1
    st.table(df[["Course", "Credit Units", "Grade", "Quality Points"]])

    # Delete Course
    course_to_remove = st.selectbox("Remove a specific course", [c["Course"] for c in st.session_state.courses])
    if st.button("Delete Selected Course"):
        st.session_state.courses = [c for c in st.session_state.courses if c["Course"] != course_to_remove]
        st.rerun()

    # Reset
    if st.checkbox("I understand this will delete all data (including history)"):
        if st.button("Reset Everything"):
            st.session_state.courses = []
            st.session_state.prev_cu = 0
            st.session_state.prev_qp = 0.0
            st.rerun()

    # CSV Export
    csv_buffer = io.BytesIO()
    summary_row = pd.DataFrame({"Course": ["TOTAL"], "Credit Units": [total_cu], "Grade": [""], "GP": [""], "Quality Points": [total_qp]})
    df_final = pd.concat([df[["Course", "Credit Units", "Grade", "GP", "Quality Points"]], summary_row], ignore_index=True)
    df_final.to_csv(csv_buffer, index=False)
    st.download_button("Download Courses (CSV)", csv_buffer.getvalue(), "courses.csv", "text/csv")
else:
    st.info("Add courses above to see your CGPA.")

st.divider()
st.caption("Powered by Team Cosmas • Support • Pray • Canvass")