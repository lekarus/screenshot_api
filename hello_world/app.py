from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()


@app.get("/hello_world")
def root():
    return {
        "message": "Hello World!",
        "status": 200
    }


lambda_handler = Mangum(app)
