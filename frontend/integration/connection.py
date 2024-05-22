import json

from .common import get_request, post_request, post_request_with_files


def get_data_source(data_source_id: int):
    path = f"data_sources/{data_source_id}"
    response = get_request(path)
    return response.json()


def get_data_sources():
    path = "data_sources/"
    response = get_request(path)
    return response.json()


def create_data_source(
        name: str,
        type: str,
        description: str,
        connection: dict
):
    path = "data_sources/"
    payload = {
        "name": name,
        "type": type,
        "description": description,
        "connection": connection
    }
    response = post_request(path, payload)
    response_dict = response.json()
    response_dict["status_code"] = response.status_code
    return response_dict


def sync_metadata(data_source_id: int):
    path = "metadata/"
    payload = {
        "data_source_id": data_source_id
    }
    response = post_request(path, payload)
    response_dict = response.json()
    response_dict["status_code"] = response.status_code
    return response_dict


def query_metadata(query: str):
    path = "metadata/query/"
    response = get_request(path, params={"query": query})
    try:
        response_dict = response.json() # This can throw an ugly exception
        response_dict["status_code"] = response.status_code
        return response_dict
    except Exception as e:
        response_dict = {}
        response_dict["text"] = response.text
        response_dict["status_code"] = response.status_code
        return response_dict


def join_data(data_source_id, table_name):
    path = "joinable_table/join_data/"
    payload = {
        "data_source_id": data_source_id,
        "table_name": table_name
    }
    print(path, payload)
    response = post_request(path, payload)
    response_dict = response.json()
    response_dict["status_code"] = response.status_code
    return response_dict


def get_table_data(data_source_id, table_name, limit=1000):
    path = f"data_sources/{data_source_id}/table_name/{table_name}"
    response = get_request(path)
    print(response.json())
    return response.json()


def post_find_schema_matching(target_file, source_file):
    path = "find_schema_matching/"
    files = {
        "target_file": (target_file.name, target_file, "text/csv"),
        "source_file": (source_file.name, source_file, "text/csv")
    }
    response = post_request_with_files(path, files)
    response_dict = response.json()
    response_dict["status_code"] = response.status_code
    
    return response_dict


def post_find_data_matching(target_file, source_file, matching):
    path = "find_data_matching/"
    files = {
        "target_file": (target_file.name, target_file, "text/csv"),
        "source_file": (source_file.name, source_file, "text/csv")
    }
    payload = {"matching": json.dumps(matching)}
    response = post_request_with_files(path, files, payload)

    return response
