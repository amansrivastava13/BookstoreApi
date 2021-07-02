from fastapi import FastAPI, Depends, HTTPException
from routes.v1 import app_v1
from routes.v2 import app_v2
from starlette.requests import Request
from utils.security import check_jwt_token
from starlette.responses import Response
from starlette.status import HTTP_401_UNAUTHORIZED
from datetime import datetime
from fastapi.security import OAuth2PasswordRequestForm
from utils.security import authenticate_user, create_jwt_token
from models.jwt_user import JWTUser
from utils.const import TOKEN_DESCRIPTION, TOKEN_SUMMARY, REDIS_URL, TESTING, IS_LOAD_TEST, REDIS_URL_PRODUCTION, \
    TOKEN_INVALID_CREDENTIALS_MSG
# from utils.const import IS_PRODUCTION
from utils.db_object import db
import utils.redis_object as re
import aioredis
from utils.redis_object import check_test_redis
import pickle
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(title="API Documentation", description="FastApi Framework", version="1.0.0")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origin=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(app_v1, prefix="/v1", dependencies=[Depends(check_jwt_token), Depends(
    check_test_redis)])  # rem ki yeh list me hi aayga. And isko call krne me yeh () nhi lgega
app.include_router(app_v2, prefix="/v2", dependencies=[Depends(check_jwt_token), Depends(check_test_redis)])


# Do something ki whenever we hit our api our db gets connected and when we shut the api db gets disconnected

# This fun runs when the api starts
@app.on_event("startup")
async def connect_db():
    if not TESTING:
        await db.connect()
        re.redis = await aioredis.create_redis_pool(REDIS_URL)
        # if IS_PRODUCTION:
        #    re.redis = await aioredis.create_redis_pool(REDIS_URL_PRODUCTION)
        # else:
        #   re.redis = await aioredis.create_redis_pool(REDIS_URL)


# This fun runs when the api shuts
@app.on_event("shutdown")
async def disconnect_db():
    if not TESTING:
        await db.disconnect()
        re.redis.close()
        await re.redis.wait_closed()


# prefix /v1 and /v2 prefix api ko hi token pe depend kra gya hey so is api ko run krna ke liye token ki need nhi hey
@app.get("/")
async def health_check():
    return {"health status": "OK"}  # you always return a json


# form url encoded
# It does not requires /v1 in its api and it no longer Depends on check_jwt_token
@app.post("/token", description=TOKEN_DESCRIPTION, summary=TOKEN_SUMMARY)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # check that this user is in our redis or not
    redis_key = f"{form_data.username}{form_data.password}"
    user = await re.redis.get(redis_key)
    if not user:
        jwt_user_dict_2 = {"username": form_data.username, "password": form_data.password}
        obj = JWTUser(**jwt_user_dict_2)
        user = await authenticate_user(obj)  # obj.username, obj.password can be accessible
        if user is None:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=TOKEN_INVALID_CREDENTIALS_MSG)
        await re.redis.set(redis_key, pickle.dumps(user))  # set krna bhi hota hi hey
    else:
        user = pickle.loads(user)
    jwt_token_2 = create_jwt_token(user)
    return {
        "access_token": jwt_token_2}
    # access_token is fixed key name for saving the jwt_token. It is a rule of FastApi for swagger documentation


# print(123)

@app.middleware("http")
async def middleware(request: Request, call_next):
    start_time = datetime.utcnow()
    response = await call_next(request)
    # modify response
    execution_time = (datetime.utcnow() - start_time).microseconds
    response.headers["x-execution-time"] = str(execution_time)
    # Headers me key and value hmesh str me hi hoti hein (remember that)
    return response
