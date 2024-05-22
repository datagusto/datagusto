import json
import os
from typing import Optional

import requests
import streamlit as st

BACKEND_ENDPOINT = os.environ["BACKEND_ENDPOINT"]

HEADERS = {
    'Content-Type': 'application/json',
}


def get_request(path: str, params=None, timeout=1200, authentication=True):
    if params is None:
        params = {}
    url = f"{BACKEND_ENDPOINT}/{path}"
    response = requests.request(
        method="GET",
        url=url,
        headers=generate_header(authentication),
        params=params,
        timeout=timeout
    )
    print(response)
    return response


def post_request(path: str, payload: dict, timeout=1200, authentication=True):
    url = f"{BACKEND_ENDPOINT}/{path}"
    response = requests.request(
        method="POST",
        url=url,
        headers=generate_header(authentication),
        timeout=timeout,
        data=json.dumps(payload)
    )
    print(response)
    print(response.text)
    return response


def post_request_with_files(path: str, files: dict, payload: Optional[dict] = None, timeout=3600):
    url = f"{BACKEND_ENDPOINT}/{path}"
    response = requests.request(
        method="POST",
        url=url,
        headers={
            'Authorization': 'Bearer ' + st.session_state.access_token
        },
        timeout=timeout,
        data=payload,
        files=files
    )
    print(response)
    return response


def generate_header(authentication=True):
    headers = HEADERS
    if authentication:
        headers['Authorization'] = 'Bearer ' + st.session_state.access_token
    return headers
