import streamlit as st
import os

from auth import is_logged_in
from navigation import go_home
from worksheet import get_metadata_form, list_worksheets


def init_page():
    st.session_state.current_data_source_id = ""
    st.session_state.just_added_new_worksheet = False

def main():
    if not is_logged_in():
        go_home()
    
    # Initialize page
    file_name = os.path.basename(__file__)
    prev_file_name = st.session_state.get("file_name", None)
    if file_name != prev_file_name:
        st.session_state.file_name = file_name
        init_page()

    # Body of the page from here

    st.header("Worksheets")

    if st.session_state.just_added_new_worksheet:
        st.session_state.just_added_new_worksheet = False
        st.session_state.adding_new_worksheet = False

    st.checkbox("Add new worksheet", key="adding_new_worksheet")

    if st.session_state.adding_new_worksheet:
        get_metadata_form()
        # add_worksheet_form()
    else:
        list_worksheets()


if __name__ == '__main__':
    main()
