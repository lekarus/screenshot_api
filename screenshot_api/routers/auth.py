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
        f"scope=openid&"
        f"redirect_uri="
        f"https://{request.scope['aws.event']['requestContext']['domainName']}/{os.getenv('StackName')}/get_token"
    )


@auth_router.get("/get_token")
async def get_token(code: str):
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
    return token
