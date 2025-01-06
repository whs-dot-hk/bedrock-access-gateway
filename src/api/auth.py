import os
from typing import Annotated

import boto3
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from api.setting import DEFAULT_API_KEYS

api_key_param = os.environ.get("API_KEY_PARAM_NAME")
api_key_env = os.environ.get("API_KEY")
if api_key_param:
    ssm = boto3.client("ssm")
    api_keys_str = ssm.get_parameter(Name=api_key_param, WithDecryption=True)["Parameter"][
        "Value"
    ]
elif api_key_env:
    api_keys_str = api_key_env
else:
    api_keys_str = DEFAULT_API_KEYS

# Convert comma-separated string to a set of API keys
api_keys = {key.strip() for key in api_keys_str.split(",")}

security = HTTPBearer()


def api_key_auth(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    if credentials.credentials not in api_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key"
        )
