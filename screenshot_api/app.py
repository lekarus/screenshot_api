from fastapi import FastAPI
from mangum import Mangum

from routers.auth import auth_router

app = FastAPI()
app.include_router(auth_router)

lambda_handler = Mangum(app)
