from fastapi import FastAPI
from mangum import Mangum

from config import settings
from routers.auth import auth_router

app = FastAPI(root_path=f"/{settings.stack_name}")
app.include_router(auth_router)

lambda_handler = Mangum(app)
