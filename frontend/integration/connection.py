import json
import os
import requests

BACKEND_ENDPOINT = os.environ["BACKEND_ENDPOINT"]


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
        owner_id: int,
        description: str,
        connection: dict
):
    path = "data_sources/"
    payload = {
        "name": name,
        "type": type,
        "owner_id": owner_id,
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


def get_request(path: str, params=None, timeout=1200):
    if params is None:
        params = {}
    url = f"{BACKEND_ENDPOINT}/{path}"
    response = requests.request(
        method="GET",
        url=url,
        params=params,
        timeout=timeout
    )
    print(response)
    return response


def post_request(path: str, payload: dict, timeout=1200):
    url = f"{BACKEND_ENDPOINT}/{path}"
    response = requests.request(
        method="POST",
        url=url,
        headers={
            'Content-Type': 'application/json'
        },
        timeout=timeout,
        data=json.dumps(payload)
    )
    print(response)
    print(response.text)
    return response


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