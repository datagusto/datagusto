import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

from auth import show_auth_page, is_logged_in, get_user_name


def init_page():
    pass


def main():
    # Initialize page
    file_name = os.path.basename(__file__)
    prev_file_name = st.session_state.get("file_name", None)
    if file_name != prev_file_name:
        st.session_state.file_name = file_name
        init_page()

    if not is_logged_in():
        show_auth_page()
    else:
        st.header("Home")
        st.write(f"Hi! You are logged in as {get_user_name()}")


if __name__ == '__main__':
    main()
