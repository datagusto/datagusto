import streamlit as st
import os

from auth import is_logged_in
from navigation import go_home
from data_sources import list_data_sources, add_data_source_form, get_default_port, data_source_types


def init_page():
    st.session_state.just_added_new_data_source = False

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

    st.header("Data Sources")
    
    if st.session_state.just_added_new_data_source:
        st.session_state.just_added_new_data_source = False
        st.session_state.adding_new_data_source = False

    st.checkbox("Add new data source", key="adding_new_data_source")

    if st.session_state.adding_new_data_source:
        st.write("### Add New Data Source")

        # Place the database type selection outside the form to avoid Streamlit issue
        db_type_selection = st.selectbox("Select Database Type", data_source_types, key="db_type_selection")

        # Determine the default port based on the selection
        default_port = get_default_port(db_type_selection)
        add_data_source_form(default_port, db_type_selection)
    else:
        list_data_sources()


if __name__ == '__main__':
    main()
