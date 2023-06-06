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
    try:
        user = idp.get_user(AccessToken=token)
    except (KeyError, idp.exceptions.NotAuthorizedException):
        raise HTTPException(status_code=400, detail="Invalid token")

    dynamo_db = boto3.client("dynamodb")
    sub = get_sub(user)

    user = dynamo_db.get_item(
        TableName=settings.user_table,
        Key={
            "id": {
                "S": sub
            }
        }
    ).get("Item")

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    subscription = dynamo_db.get_item(
        TableName=settings.subscription_table,
        Key={
            "id": {
                "S": user["subscription"]["S"]
            }
        }
    ).get("Item")

    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")

    return User(
        id=sub,
        subscription=Subscription(
            id=subscription["id"]["S"],
            subscription_name=subscription["subscription_name"]["S"],
            storage_limit=subscription["storage_limit"]["N"],
            cost=subscription["cost"]["N"],
        )
    )


def get_bucket_name(sub: str):
    return f"screenshot-storage-{sub}"
