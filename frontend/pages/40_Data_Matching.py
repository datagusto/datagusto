import streamlit as st

from auth import is_logged_in
from navigation import go_home
from integration.connection import post_find_schema_matching, post_find_data_matching


def main():
    if not is_logged_in():
        go_home()

    if "succeeded_schema_matching" not in st.session_state:
        st.session_state.succeeded_schema_matching = False
    if "schema_matching_result" not in st.session_state:
        st.session_state.schema_matching_result = {}
    if "submit_upload_files" not in st.session_state:
        st.session_state.submit_upload_files = False
    if "submit_match_data" not in st.session_state:
        st.session_state.submit_match_data = False


    st.title("Data Matching")

    st.info("Please note that this feature is an experimental version and executing it may consume a significant number of tokens of your LLM service.")

    st.header("Step1: Upload CSV files to match data.")
    target_file = st.file_uploader("Target Data: Choose a CSV file to be integrated:", type="csv")
    source_file = st.file_uploader("Source Data: Choose a CSV file you want to integrate into the above file:", type="csv")
    st.session_state.submit_upload_files = st.button("Upload")

    if st.session_state.get("submit_upload_files", False):
        if target_file and source_file:
            result = post_find_schema_matching(target_file, source_file)
            status_code = result.pop("status_code", 200)

            if status_code == 200:
                st.session_state.succeeded_schema_matching = True
                st.session_state.schema_matching_result = result
            else:
                st.session_state.succeeded_schema_matching = False
                st.error("Something went wrong. Please try again.")
        else:
            st.warning("Choose both CSV files to upload.")
    
    if st.session_state.get("succeeded_schema_matching", False):
        st.header("Step2: Review the schema matching results.")
        st.write("Please review the schema matching results below.")

        result = st.session_state.schema_matching_result
        target_matched_columns = st.multiselect("Matched columns in target data:", result["target_data_columns"], result["target_data_matched_columns"])
        source_matched_columns = st.multiselect("Matched columns in source data:", result["source_data_columns"], result["source_data_matched_columns"])

        st.header("Step3: Match data.")
        st.write("Execute data matching with the selected columns.")
        st.session_state.submit_match_data = st.button("Match Data")

    
    if st.session_state.get("submit_match_data", False):
        # matching = st.session_state.schema_matching_result["matching"]
        # test_req(target_file, source_file, matching)
        if target_matched_columns and source_matched_columns:
            matching = st.session_state.schema_matching_result["matching"]
            response = post_find_data_matching(target_file, source_file, matching)

            if response.status_code == 200:
                st.header("Step4: Download matched data.")
                st.success("Data matching is successful. Please download the matched data below.")
                
                csv_data = response.content
                
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name="data.csv",
                    mime="text/csv"
                )
            else:
                st.error("Something failed to match data. Please try again.")


if __name__ == '__main__':
    main()
