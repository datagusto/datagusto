import streamlit as st
import json
import pandas as pd

from auth import get_user_name
from data_sources import get_data_source
from models import Worksheet
from integration.connection import query_metadata, join_data, get_table_data


def save_worksheet(worksheet_name, prompt, data_source_id, username):
    if any(not var for var in [worksheet_name, prompt, data_source_id, username]):
        st.error("Some fields are empty")
        return

    # session = Session()
    try:
        new_worksheet = Worksheet(
            worksheet_name=worksheet_name,
            prompt=prompt,
            data_source_id=data_source_id, # int
            username=username,
            # metadata="", # default ""
            # preview_data=None, # DataFrame, default None
            # data=None, # DataFrame, default None   
        )
        
        # TODO: Add new worksheet here

        st.success("New worksheet added successfully!")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        pass


def list_worksheets():
    worksheets = []

    if len(worksheets) == 0:
        st.write("No worksheets have been added yet.")
        return

    for worksheet in worksheets:
        data_source_id = worksheet.data_source_id
        ds = get_data_source(data_source_id)
            
        with st.container(border=True):
            st.write(f"Worksheet Name:\n{worksheet.worksheet_name}")
            st.write(f"prompt:\n{worksheet.prompt}")

            with st.expander("Worksheet details"):

                if ds:
                    with st.container(border=True):
                        st.markdown(ds.get_details_markdown())

                # Add more worksheet details as needed

                # edit_button, delete_button = st.columns(2)
                
                col1, col2, col3 = st.columns([1,1,1])
                
                with col1:
                    edit_button = st.button("Edit", key=f"edit_{worksheet.id}", disabled=True)
                with col2:
                    delete_button = st.button("Delete", key=f"delete_{worksheet.id}", disabled=True)
                with col3:
                    delete_check_button = st.checkbox("Check to delete", key=f"delete_check_{worksheet.id}", disabled=True)

                if edit_button:
                    # This will open the edit form with pre-filled data
                    edit_worksheet(worksheet.id)
                
                if delete_button and delete_check_button:
                    # TODO: Implement delete logic
                    st.rerun()

                # if st.button("Visualize SQL", key=f"visualize_sql_{worksheet.id}"):
                #     show_visualized_sql(worksheet.sql)
                #     show_visualization_guide()

                # Button to preview SQL results
                if st.button('Preview SQL Results', key=f"preview_sql_results_{worksheet.id}", disabled=True):
                    pass
                    # try:
                    #     preview_df = run_sql_query(worksheet.data_source_id, worksheet.sql, preview=True)
                    #     st.dataframe(preview_df)
                    # except Exception as e:
                    #     st.error(f"Failed to run SQL query: {e}")

                # Button to run SQL and download full results
                if st.button('Download Full Results', key=f"sql_results_{worksheet.id}", disabled=True):
                    pass
                    # try:
                    #     full_df = run_sql_query(worksheet.data_source_id, worksheet.sql, preview=False)
                    #     csv = full_df.to_csv(index=False).encode('utf-8')
                    #     st.download_button(
                    #         label="Download CSV",
                    #         data=csv,
                    #         file_name="sql_query_results.csv",
                    #         mime="text/csv",
                    #     )
                    # except Exception as e:
                    #     st.error(f"Failed to run SQL query: {e}")


def delete_worksheet(session, worksheet_id):
    pass

def save_worksheet_changes():
    pass

def edit_worksheet(worksheet_id):
    pass


def add_worksheet_form():
    username = get_user_name()
    data_source_id = ""
    if "my_username" not in st.session_state or not st.session_state.my_username:
        st.session_state.my_username = username

    st.write("### Add New Worksheet")
    # show_select_data_source_dropdown(data_source_id)
    
    with st.form("add_worksheet"):
        # Form fields for the worksheet's details
        worksheet_name = st.text_input("Worksheet Name")
        st.text_area("What do you want to do with your data? / What data do you want?", key="my_prompt")
        
        submit_button = st.form_submit_button("Add Worksheet")
        
        if submit_button:
            data_source_id = st.session_state.current_data_source_id
            my_prompt = st.session_state.my_prompt
            my_username = st.session_state.my_username
            save_worksheet(worksheet_name, my_prompt, data_source_id, my_username)


def set_current_table_name():
    table_name_option_selected = st.session_state.table_name_option_selected
    st.session_state.current_table_name = table_name_option_selected


def clear_worksheet():
    st.session_state.my_prompt = ""
    if "found_tables" in st.session_state:
        del st.session_state["found_tables"]
    if "current_table_name" in st.session_state:
        del st.session_state["current_table_name"]
    if "mapped_data" in st.session_state:
        del st.session_state["mapped_data"]
    st.session_state.succeed_query = False
    st.session_state.succeed_mapping = False

def get_metadata_form():
    username = get_user_name()
    data_source_id = ""
    if "my_username" not in st.session_state or not st.session_state.my_username:
        st.session_state.my_username = username

    st.write("### Integrate Data")
    # show_select_data_source_dropdown(data_source_id)
    
    if "succeed_query" not in st.session_state:
        st.session_state.succeed_query = False

    st.button("Clear data", on_click=clear_worksheet)

    with st.form("get_metadata"):
        st.text_area("What do you want to do with your data? / What data do you want?", key="my_prompt")

        query_metadata_button = st.form_submit_button("Discover data")

        if query_metadata_button:
            my_prompt = st.session_state.my_prompt
            if not my_prompt:
                st.warning("Please enter the required fields")
            else:
                with st.spinner():
                    result = query_metadata(query=my_prompt)
                    status_code = result.pop("status_code", 200)
                    
                    if status_code == 200:
                        formatted_json = json.dumps(result, indent=4)
                        # st.code(f"Results:\n\n{formatted_json}")
                        if "found_tables" not in st.session_state:
                            st.session_state.found_tables = {}
                        st.session_state.found_tables = result
                        st.session_state.succeed_query = True
                        if bool(result) is False:
                            st.warning("No relevant data was found.")
                            st.session_state.succeed_query = False
                    else:
                        st.error(f"Error getting results:\n\n{result}")
                        st.session_state.succeed_query = False

    if "succeed_mapping" not in st.session_state:
        st.session_state.succeed_mapping = False
    
    if st.session_state.succeed_query:
        # show select menu of tables
        found_tables = st.session_state.found_tables

        found_tables = []
        for data_source_id, data_dict in st.session_state.found_tables.items():
            for table, d_dict in data_dict.items():
                found_tables.append(d_dict)

        if "current_table_name" not in st.session_state or st.session_state.current_table_name == "":
            st.session_state.current_table_name = None

        # show found tables
        st.write("### Results")
        st.write(f"{len(found_tables)} relevant data were found.")
        for i, t in enumerate(found_tables):
            if "sample_data" in t:
                with st.container(border=True):
                    st.write(f"##### {t['table_name']}")
                    st.caption(f'Location: {t["data_source_name"]} / {t["database_name"]} / {t["table_name"]}')
                    # show sample data
                    st.write("**Data preview:**")
                    df = pd.read_json(t["sample_data"], orient="records")
                    st.dataframe(df)

                    # Download whole data (limit to 1000 records)
                    st.download_button(
                        label="Download",
                        data=create_download_data(data_source_id=t['data_source_id'], table_name=t['table_name']),
                        file_name=f"{t['data_source_id']}_{t['data_source_name']}_{t['database_name']}_{t['table_name']}.csv",
                        mime='text/csv',
                    )
                

        options = list(range(len(found_tables)))
        st.selectbox(
            "Please select the data you want to see in detail:", 
            options, 
            key="table_name_option_selected", 
            on_change=set_current_table_name,
            format_func=lambda x: found_tables[x]["table_name"],
            index=None
        )

        tid = st.session_state.current_table_name
        if tid is not None:
            table_name = found_tables[tid]["table_name"]
            with st.form("join_data"):
                tid = st.session_state.current_table_name
                data_source_id = found_tables[tid]["data_source_id"]

                with st.spinner():
                    if "mapped_data" not in st.session_state:
                        result = join_data(data_source_id=data_source_id, table_name=table_name)
                        status_code = result.pop("status_code", 200)

                        if status_code == 200:
                            if "mapped_data" not in st.session_state:
                                st.session_state.mapped_data = []

                            for target_data_source_id, tables in result["data"].items():
                                for target_table_name, info in tables.items():
                                    # convert back json to DataFrame
                                    info["data"] = pd.read_json(info["data"], orient="records")

                                    st.session_state.mapped_data.append({
                                        "table_name": target_table_name,
                                        "joinable_columns": [t[-1] for t in info["columns"]],
                                        "data": info["data"]
                                    })
                        else:
                            st.error(f"Error getting results:\n\n{result}")

                    if "mapped_data" in st.session_state:
                        st.write("#### The following mappable data was found")
                        for item in st.session_state.mapped_data:
                            st.write(f"##### {item['table_name']}")
                            st.write(f"- joinable columns: ({item['joinable_columns']})")
                    else:
                        st.error(f"Error getting results:\n\n{result}")

                st.write(f"Do you want to integrate {table_name} with those data?")
                mapping_data_button = st.form_submit_button("Execute data mapping")
                
            if mapping_data_button:
                st.session_state.succeed_mapping = True
                st.write("Preview data (first 10 records)")
                for item in st.session_state.mapped_data:
                    st.write(f"Table: {item['table_name']}")
                    st.dataframe(item['data'].head(10))

                    csv = item['data'].to_csv(index=False)
                    st.download_button(
                        label=f"Download as CSV ({item['table_name']})",
                        data=csv,
                        file_name=f"{table_name}_{item['table_name']}_data.csv",
                        mime="text/csv"
                    )


def create_download_data(data_source_id, table_name):
    response = get_table_data(data_source_id, table_name)
    df = pd.read_json(response["data"], orient="records")
    csv = df.to_csv(index=False)
    return csv
