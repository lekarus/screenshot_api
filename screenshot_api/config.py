import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    user_table: str = os.getenv("UserTable")
    subscription_table: str = os.getenv("SubscriptionTable")
    cognito_domain: str = os.getenv('CognitoDomain')
    region: str = os.getenv('Region')
    user_pool_id: str = os.getenv("UserPoolId")
    stack_name: str = os.getenv('StackName')
    google_client_id: str = os.getenv("GoogleClientId")
    bucket_name: str = os.getenv("S3Bucket")
    base_subscription_id: str = "1"


settings = Settings()
