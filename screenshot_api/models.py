from pydantic import BaseModel


class Subscription(BaseModel):
    id: int
    subscription_name: str
    storage_limit: int
    cost: int


class User(BaseModel):
    sub: str
    subscription: Subscription
