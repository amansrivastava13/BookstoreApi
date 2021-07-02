from fastapi import FastAPI, APIRouter
app_v2 = APIRouter() # First step of versioning

@app_v2.get("/hello")
async def my_first_api():
    return {"This is my version 2"}
