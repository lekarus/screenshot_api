import os
from typing import Annotated

import boto3
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    storage_limit: int


def get_sub(user: dict):
    for attribute in user["UserAttributes"]:
        if attribute["Name"] == "sub":
            return attribute["Value"]


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    idp = boto3.client("cognito-idp")
    dynamo_db = boto3.client("dynamodb")
    try:
        user = idp.get_user(AccessToken=token)
        sub = get_sub(user)
        subscription = dynamo_db.get_item(
            TableName=os.getenv("UserTable"),
            Key={
                "id": {
                    "S": sub
                }
            }
        )["Item"]["subscription"]["N"]

        storage_limit = dynamo_db.get_item(
            TableName=os.getenv("SubscriptionTable"),
            Key={
                "id": {
                    "S": subscription
                }
            }
        )["Item"]["storage_limit"]["S"]

        return User(
            username=sub, storage_limit=storage_limit
        )
    except (KeyError, idp.exceptions.NotAuthorizedException):
        raise HTTPException(status_code=400, detail="Invalid token")
