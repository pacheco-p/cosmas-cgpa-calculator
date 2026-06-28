import streamlit as st
import database

st.set_page_config(
    page_title="Cosmas CGPA Calculator",
    page_icon="🎓",
    layout="wide"
)

database.init_db()

st.title("🏛️ COSMAS AT SUG TOP SEAT")
st.caption("Support • Pray • Canvass")

st.success("Database initialized successfully ✅")