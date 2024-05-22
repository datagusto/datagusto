import streamlit as st
import time
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
import json
from urllib.parse import quote_plus

import integration.connection as conn
from auth import is_logged_in
from models import DataSource, data_source_types


def view_data_source_details(ds: DataSource):
    st.markdown(ds.get_details_markdown())
#     st.markdown(f"""
# Data source details:
# - **Connection Name:** `{ds.name}`
# - **Database Type:** `{ds.dtype}`
# - **Description:** `{ds.description}`
# - **Hostname:** `{ds.hostname}`
# - **Port:** `{ds.port}`
# - **Database Name:** `{ds.database_name}`
# - **Username:** `{ds.owner_id}`
# - **Password:** `{'*' * len(ds.password)}`
# """)


def list_data_sources():
    with st.spinner():
        data_dicts = conn.get_data_sources()

    # Parse the JSON array string into Python list of dictionaries
    # data_dicts = json.loads(json_array_str)

    # Convert each dictionary to a DataSource instance
    data_sources = [DataSource.from_dict(data_dict) for data_dict in data_dicts]
    
    if not data_sources:  # Check if the list is empty
        st.write("No data sources have been added yet.")
    else:
        for ds in data_sources:
            with st.container(border=True):
                col1, col2 = st.columns([5,1])
                with col1:
                    st.write(f"#### {ds.name}  ({ds.dtype})")
                    st.write(f"Description: {ds.description}")
                    view_checkbox = st.checkbox("Show Details", key=f"view_data_source_{ds.id}")
                with col2:
                    delete_button = st.button("Delete", key=f"delete_{ds.id}", disabled=True)
                    delete_check_button = st.checkbox("Check to delete", key=f"delete_check_{ds.id}", disabled=True)
                
                if view_checkbox:
                    # This will open the edit form with pre-filled data
                    view_data_source_form(ds.id)
                    pass
                
                if delete_button and delete_check_button:
                    # Implement delete logic
                    pass
                    # st.rerun()

def set_current_data_source_id():
    data_source_option_selected = st.session_state.data_source_option_selected
    data_source_options_dict = st.session_state.data_source_options_dict
    current_data_source_id = data_source_options_dict[data_source_option_selected]
    st.session_state.current_data_source_id = current_data_source_id
    

def show_select_data_source_dropdown(data_source_id=""):
    # st.session_state.current_data_source_id = data_source_id

    data_dicts = conn.get_data_sources()
    data_sources = [DataSource.from_dict(data_dict) for data_dict in data_dicts]
    
    if not data_sources:  # Check if the list is empty
        st.write("No data sources have been added yet.")
    else:
        options_dict = {f"{index}: {ds.name} (Type: {ds.dtype})": ds.id for index, ds in enumerate(data_sources, start=1)}
        options = list(options_dict.keys())
        
        st.session_state.data_source_options_dict = options_dict

        data_source_option_selected_index = 0
        if "current_data_source_id" not in st.session_state or st.session_state.current_data_source_id == "":
            st.session_state.current_data_source_id = data_sources[0].id
        
        for index, ds in enumerate(data_sources):
            if "current_data_source_id" in st.session_state and st.session_state.current_data_source_id == ds.id:
                data_source_option_selected_index = index

        if not data_source_id:
            # Create the selectbox (dropdown menu)
            st.selectbox('Choose a Data Source:', options, index=data_source_option_selected_index,
                         key="data_source_option_selected", on_change=set_current_data_source_id)
     
        ds = data_sources[data_source_option_selected_index]
        with st.container(border=True):
            st.write(f"#### {data_source_option_selected_index + 1}: {ds.name} (Type: {ds.dtype})")
            st.write(f"Description: {ds.description}")
            view_data_source_details(ds)


def save_data_source_changes():
    name = st.session_state['Connection Name']
    description = st.session_state['Description']
    dtype = st.session_state['Database Type']
    hostname = st.session_state['Hostname']
    port = st.session_state['Port']
    database_name = st.session_state['Database Name']
    username = st.session_state['Username']
    password = st.session_state['Password']
    ds_id = st.session_state['ds_id']

    try:
        data_dict = conn.get_data_source(ds_id)
        ds = DataSource.from_dict(data_dict)

        if not ds:
            st.error(f"Data Source not found. id = {ds_id}")
            return
        
        if ds:
            ds.name = name
            ds.description = description
            ds.dtype = dtype
            ds.hostname = hostname
            ds.port = port
            ds.database_name = database_name
            ds.username = username
            ds.password = password
            
            # TODO: Update data source here

            st.success("Data source updated successfully!")
        else:
            st.error("Data source not found.")
    except Exception as e:
        st.error(f"An error occurred: {e}")


def get_data_source(ds_id):
    data_dict = conn.get_data_source(ds_id)
    
    if data_dict:
        ds = DataSource.from_dict(data_dict)
        return ds
    else:
        return None

def view_data_source_form(ds_id):
    ds = get_data_source(ds_id)

    if not ds:
        st.error(f"Data Source not found. id = {ds_id}")
        return
    
    with st.form(f"view_data_source_{ds_id}"):
        st.text_input("Connection Name", value=ds.name, key='Connection Name')
        st.text_area("Description", value=ds.description, key='Description')
        st.selectbox("Database Type", data_source_types, index=data_source_types.index(ds.dtype),
                     key='Database Type')
        st.text_input("Hostname", value=ds.hostname, key='Hostname')
        st.number_input("Port", value=ds.port, key='Port')
        st.text_input("Database Name", value=ds.database_name, key='Database Name')
        st.text_input("Username", value=ds.username, key='Username')
        st.text_input("Password", type="password", key='Password')
        
        # Include the data source ID in session state to access in the save function
        st.session_state['ds_id'] = ds_id
        
        st.form_submit_button("Save Changes", on_click=save_data_source_changes, disabled=True)


def test_connection(dtype, username, password, hostname, port, database_name):
    password = quote_plus(password)
    """Attempt to connect to the database and return the result."""
    # Construct the connection string
    if dtype == "mysql":
        engine_string = f"mysql+pymysql://{username}:{password}@{hostname}:{port}/{database_name}?connect_timeout=10"
    elif dtype == "postgresql":
        engine_string = f"postgresql+psycopg2://{username}:{password}@{hostname}:{port}/{database_name}?connect_timeout=10"
    else:
        return "Unsupported database type"
    
    try:
        # Attempt to create an engine and connect to the database
        engine = sqlalchemy.create_engine(engine_string)
        with engine.connect() as conn:
            # If connection is successful
            return "Success"
    except SQLAlchemyError as e:
        # If there is an error connecting to the database
        return str(e)

# Function to update the port based on database type selection
def get_default_port(db_type):
    return 3306 if db_type == "mysql" else 5432


def add_data_source_form(default_port, selected_db_type):
    if not is_logged_in():
        st.error("Looks like you are not logged in yet! Please log in first.")
        return
    
    with st.form("add_data_source"):
        name = st.text_input("Connection Name")
        description = st.text_area("Description")
        # Use the selected_db_type and default_port from outside the form
        dtype = st.selectbox("Database Type", data_source_types, index=data_source_types.index(selected_db_type),
                             disabled=True)
        hostname = st.text_input("Hostname")
        port = st.number_input("Port", value=default_port)  # Use the default port here
        database_name = st.text_input("Database Name")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        col1, col2 = st.columns(2)
        with col1:
            test_button = st.form_submit_button("Test Data Source", on_click=lambda: st.session_state.update({"test_clicked": True}))
        with col2:
            submit_button = st.form_submit_button("Add Data Source", disabled=st.session_state.just_added_new_data_source)
        
        mandatory_fields = [name, description, dtype, hostname, port, database_name, username, password]
        missing_fields = [field_name for field_name, field_value in zip(["name", "description", "database type", "hostname", "port", "database name", "username", "password"], mandatory_fields) if not field_value]

        if test_button or submit_button:
            if missing_fields:
                st.error(f"Missing mandatory field(s): {', '.join(missing_fields)}")
            else:
                if 'test_clicked' in st.session_state and st.session_state.test_clicked:
                    test_result = test_connection(dtype, username, password, hostname, port, database_name)
                    if test_result == "Success":
                        st.success("Connection test succeeded.")
                    else:
                        st.error(f"Connection test failed: {test_result}")
                    st.session_state.test_clicked = False  # Reset test state after showing result

        if submit_button and not missing_fields:
            with st.status("In progress... (this may take a while)"):
                # add connection
                st.write("Registering data source...")
                connection = {
                    "host": hostname,
                    "port": port,
                    "username": username,
                    "password": password,
                    "database": database_name
                }
                result = conn.create_data_source(name, dtype, description, connection)
                status_code = result.pop("status_code", 200)

                if status_code != 200:
                    st.error(f"Error adding data source:\n\n{result}")
                
                # create metadata
                st.write("Scanning the data source...")
                data_source_id = result.get("id")
                result = conn.sync_metadata(data_source_id=data_source_id)
                status_code = result.pop("status_code", 200)

                if status_code != 200:
                    st.error(f"Error adding data source:\n\n{result}")

            if status_code == 200:
                st.success("Data source added successfully!")
                st.session_state.just_added_new_data_source = True
                time.sleep(3)
                st.rerun()
            else:
                st.error(f"Error adding data source:\n\n{result}")

