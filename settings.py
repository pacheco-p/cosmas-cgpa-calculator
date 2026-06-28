import streamlit as st
import database


def show():

    st.title("⚙️ Settings")

    st.subheader("🔒 Change Password")

    current_password = st.text_input(
        "Current Password",
        type="password"
    )

    new_password = st.text_input(
        "New Password",
        type="password"
    )

    confirm_password = st.text_input(
        "Confirm New Password",
        type="password"
    )

    if st.button("Update Password"):

        database.cursor.execute(
            """
            SELECT password
            FROM users
            WHERE username=?
            """,
            (st.session_state.username,)
        )

        user = database.cursor.fetchone()

        if not user:

            st.error("User not found.")

        elif user[0] != current_password:

            st.error("Current password is incorrect.")

        elif new_password != confirm_password:

            st.error("Passwords do not match.")

        elif len(new_password) < 6:

            st.warning("Password must be at least 6 characters.")

        else:

            database.cursor.execute(
                """
                UPDATE users
                SET password=?
                WHERE username=?
                """,
                (
                    new_password,
                    st.session_state.username
                )
            )

            database.conn.commit()

            st.success("Password updated successfully!")

    st.divider()

    st.subheader("🗑 Reset History")

    if st.checkbox("I understand this will permanently delete all my saved calculations"):

        if st.button("Delete All History"):

            database.cursor.execute(
                """
                DELETE FROM history
                WHERE username=?
                """,
                (st.session_state.username,)
            )

            database.conn.commit()

            st.success("History deleted successfully.")

    st.divider()

    st.subheader("❌ Delete Account")

    if st.checkbox("I understand this action cannot be undone"):

        if st.button("Delete My Account"):

            database.cursor.execute(
                """
                DELETE FROM history
                WHERE username=?
                """,
                (st.session_state.username,)
            )

            database.cursor.execute(
                """
                DELETE FROM users
                WHERE username=?
                """,
                (st.session_state.username,)
            )

            database.conn.commit()

            st.session_state.logged_in = False
            st.session_state.username = ""

            st.success("Account deleted successfully.")

            st.rerun()

    st.divider()

    st.subheader("ℹ About")

    st.info("""
**Cosmas CGPA Calculator**

🏛 Team Cosmas

Support • Pray • Canvass

Version 1.0
    """)
