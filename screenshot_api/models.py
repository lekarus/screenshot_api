from pydantic import BaseModel


class Subscription(BaseModel):
    id: str
    subscription_name: str
    storage_limit: int
    cost: int


class User(BaseModel):
    id: str
    subscription: Subscription
