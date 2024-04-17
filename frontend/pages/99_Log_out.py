import streamlit as st
import os

from auth import show_logout_page, is_logged_in
from navigation import go_home

def init_page():
    pass

def main():
    if not is_logged_in():
        go_home

    # Initialize page
    file_name = os.path.basename(__file__)
    prev_file_name = st.session_state.get("file_name", None)
    if file_name != prev_file_name:
        st.session_state.file_name = file_name
        init_page()

    show_logout_page()

if __name__ == '__main__':
    main()
