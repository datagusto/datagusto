import json
from typing import Any

from .common import get_request, post_request, post_request_with_files, delete_request


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

def delete_data_source(data_source_id: int):
    path = f"data_sources/{data_source_id}"
    response = delete_request(path)
    response_dict = response.json()
    response_dict["status_code"] = response.status_code
    return response_dict

def create_data_source_as_file(
        name: str,
        type: str,
        description: str,
        connection: dict,
        file: Any,
        file_type: str
):
    path = "data_sources/file/"

    files = {
        "file": (file.name, file, "text/csv"),
    }
    payload = {"detail": json.dumps({
        "name": name,
        "type": type,
        "description": description,
        "file_type": file_type,
    })}
    response = post_request_with_files(path, files, payload)
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
    path = "joinable/join_data/"
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
    path = "matching/find_schema/"
    files = {
        "target_file": (target_file.name, target_file, "text/csv"),
        "source_file": (source_file.name, source_file, "text/csv")
    }
    # processing might take a while, so increase the timeout to 5 hours
    response = post_request_with_files(path, files, timeout=18000)
    response_dict = response.json()
    response_dict["status_code"] = response.status_code
    
    return response_dict


def post_find_data_matching(target_file, source_file, matching):
    path = "matching/find_data/"
    files = {
        "target_file": (target_file.name, target_file, "text/csv"),
        "source_file": (source_file.name, source_file, "text/csv")
    }
    payload = {"matching": json.dumps(matching)}
    # processing might take a while, so increase the timeout to 5 hours
    response = post_request_with_files(path, files, payload, timeout=18000)

    return response


def post_generate_erd(data_source_id):
    path = f"analysis/erd/{data_source_id}"
    response = post_request(path, {})
    response_dict = response.json()
    response_dict["status_code"] = response.status_code
    return response_dict
