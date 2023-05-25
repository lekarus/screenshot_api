from typing import Annotated

import boto3
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from config import settings
from models import User, Subscription

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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
        subscription_id = dynamo_db.get_item(
            TableName=settings.user_table,
            Key={
                "id": {
                    "S": sub
                }
            }
        )["Item"]["subscription"]["S"]
        subscription = dynamo_db.get_item(
            TableName=settings.subscription_table,
            Key={
                "subscription_name": {
                    "S": subscription_id
                }
            }
        )["Item"]

        return User(
            sub=sub, subscription=Subscription(
                id=subscription["id"]["S"],
                subscription_name=subscription["subscription_name"]["S"],
                storage_limit=subscription["storage_limit"]["N"],
                cost=subscription["cost"]["N"],
            )
        )
    except (KeyError, idp.exceptions.NotAuthorizedException):
        raise HTTPException(status_code=400, detail="Invalid token")
