# encoding: utf-8
import requests

from .config import config
from .compat import OK

from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

disable_warnings(InsecureRequestWarning)


def get_new_token(username=config.get("username"), password=config.get("password")):
    """

    Args:
        username (str):
        password (str):

    Returns:
        Bear Token (str)
    """

    token_url = config.get("base_url") + "/cxrestapi/auth/identity/connect/token"

    req_data = {
        "username": username,
        "password": password,
        "grant_type": "password",
        "scope": "sast_api",
        "client_id": "resource_owner_sast_client",
        "client_secret": "014DF517-39D1-4453-B7B3-9930C563627C"
    }

    response = requests.post(url=token_url, data=req_data, verify=False)

    if response.status_code != OK:
        raise ValueError(response.text, response.status_code)

    content = response.json()
    return content.get("token_type") + " " + content.get("access_token")
