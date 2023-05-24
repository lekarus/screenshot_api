import os

import boto3
import requests
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from starlette.requests import Request

auth_router = APIRouter()


@auth_router.get("/login")
def login(request: Request):
    idp = boto3.client("cognito-idp")
    client_id = idp.list_user_pool_clients(UserPoolId=os.getenv("UserPoolId"))["UserPoolClients"][0]["ClientId"]
    return RedirectResponse(
        f"https://{os.getenv('CognitoDomain')}.auth.{os.getenv('Region')}.amazoncognito.com/oauth2/authorize?"
        f"client_id={client_id}&"
        f"response_type=code&"
        f"scope=aws.cognito.signin.user.admin+email+openid+phone+profile&"
        f"redirect_uri="
        f"https://{request.scope['aws.event']['requestContext']['domainName']}/{os.getenv('StackName')}/get_token"
    )


@auth_router.get("/get_token")
def get_token(code: str):
    idp = boto3.client("cognito-idp")
    client_id = idp.list_user_pool_clients(UserPoolId=os.getenv("UserPoolId"))["UserPoolClients"][0]["ClientId"]
    client = idp.describe_user_pool_client(UserPoolId=os.getenv("UserPoolId"), ClientId=client_id)
    token = requests.post(
        f"https://{os.getenv('CognitoDomain')}.auth.{os.getenv('Region')}.amazoncognito.com/oauth2/token",
        data={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": client_id,
            "redirect_uri": client["UserPoolClient"]["CallbackURLs"][0],
        }
    ).json()
    username = idp.get_user(AccessToken=token["access_token"])["Username"]

    dynamo_db = boto3.client('dynamodb')
    if not dynamo_db.get_item(
            TableName=os.getenv("UserTable"),
            Key={
                "id": {
                    "S": username,
                }
            }
    ).get("Item"):
        dynamo_db.put_item(
            TableName=os.getenv("UserTable"),
            Item={
                "id": {
                    "S": username,
                },
                "subscription": {
                    "N": "1",
                }
            }
        )
    return token
