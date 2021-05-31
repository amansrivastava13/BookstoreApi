from fastapi import FastAPI
app_v2 = FastAPI(openapi_prefix='/v2') # First step of versioning

@app_v2.get("/hello")
async def my_first_api():
    return {"This is my version 2"}
