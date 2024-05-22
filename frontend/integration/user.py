
from .common import get_request, post_request, post_request_with_files


def signup(username: str, password: str):
    path = "user/"
    payload = {
        "username": username,
        "password": password
    }
    response = post_request(path, payload, authentication=False)
    response_dict = response.json()
    response_dict["status_code"] = response.status_code
    print(response)
    print(response_dict)
    return response_dict


def login(username: str, password: str):
    path = "user/login/"
    payload = {
        "username": username,
        "password": password
    }
    response = post_request(path, payload, authentication=False)
    response_dict = response.json()
    response_dict["status_code"] = response.status_code
    print(response)
    print(response_dict)
    return response_dict
