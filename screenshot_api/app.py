from fastapi import FastAPI
from mangum import Mangum

from routers.auth import auth_router
from routers.screenshot import screenshot_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(screenshot_router)

lambda_handler = Mangum(app)
