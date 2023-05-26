import boto3
import requests
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from starlette.exceptions import HTTPException
from starlette.requests import Request

from config import settings
from utils.auth import get_sub

auth_router = APIRouter()


@auth_router.get("/login")
def login(request: Request):
    idp = boto3.client("cognito-idp")
    client_id = idp.list_user_pool_clients(UserPoolId=settings.user_pool_id)["UserPoolClients"][0]["ClientId"]
    return RedirectResponse(
        f"https://{settings.cognito_domain}.auth.{settings.region}.amazoncognito.com/oauth2/authorize?"
        f"client_id={client_id}&"
        f"response_type=code&"
        f"scope=aws.cognito.signin.user.admin+email+openid+phone+profile&"
        f"redirect_uri="
        f"https://{request.scope['aws.event']['requestContext']['domainName']}/{settings.stack_name}/get_token"
    )


@auth_router.get("/get_token")
def get_token(code: str):
    idp = boto3.client("cognito-idp")
    client = idp.describe_user_pool_client(UserPoolId=settings.user_pool_id, ClientId=settings.google_client_id)
    try:
        token = requests.post(
            f"https://{settings.cognito_domain}.auth.{settings.region}.amazoncognito.com/oauth2/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": settings.google_client_id,
                "redirect_uri": client["UserPoolClient"]["CallbackURLs"][0],
            }
        ).json()
        sub = get_sub(idp.get_user(AccessToken=token["access_token"]))
    except (idp.exceptions.NotAuthorizedException, KeyError):
        raise HTTPException(status_code=400, detail="Invalid token")

    dynamo_db = boto3.client('dynamodb')

    if not dynamo_db.get_item(
            TableName=settings.user_table,
            Key={
                "id": {
                    "S": sub,
                }
            }
    ).get("Item"):
        dynamo_db.put_item(
            TableName=settings.user_table,
            Item={
                "id": {
                    "S": sub,
                },
                "subscription": {
                    "S": settings.base_subscription_id,
                }
            }
        )
    return token
