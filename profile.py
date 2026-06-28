import streamlit as st

def show():

    st.title("👤 My Profile")

    st.write("### Username")

    st.success(
        st.session_state.username
    )

    st.write("---")

    st.info(
        "More profile features coming soon."
    )