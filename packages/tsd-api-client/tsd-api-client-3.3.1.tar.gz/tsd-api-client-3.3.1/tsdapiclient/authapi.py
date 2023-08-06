
"""Module for the TSD Auth API."""

import json
import requests

from tsdapiclient.client_config import ENV
from tsdapiclient.tools import handle_request_errors, auth_api_url

@handle_request_errors
def get_jwt_basic_auth(env, pnum, api_key, token_type='import'):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    url = f'{auth_api_url(env, pnum, "basic")}?type={token_type}'
    try:
        resp = requests.post(url, headers=headers)
    except Exception as e:
        raise e
    if resp.status_code in [200, 201]:
        token = json.loads(resp.text)['token']
        return token
    else:
        return None

@handle_request_errors
def get_jwt_tsd_auth(
    env,
    pnum,
    api_key,
    user_name,
    password,
    otp,
    token_type
):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    data = {
        'user_name': user_name,
        'password': password,
        'otp': otp
    }
    url = f'{auth_api_url(env, pnum, "tsd")}?type={token_type}'
    try:
        resp = requests.post(url, data=json.dumps(data), headers=headers)
    except Exception as e:
        raise e
    if resp.status_code in [200, 201]:
        token = json.loads(resp.text)['token']
        return token
    else:
        return None
