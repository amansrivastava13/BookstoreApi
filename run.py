from fastapi import FastAPI
from routes.v1 import app_v1
from routes.v2 import app_v2
from starlette.requests import Request
from utils.security import check_jwt_token
from starlette.responses import Response
from starlette.status import HTTP_401_UNAUTHORIZED
from datetime import datetime

app = FastAPI()
app.mount("/v1", app_v1) #Second and final step of versioning
app.mount("/v2", app_v2)

# print(123)

# In Middle we can return only Response object from starlette.responses so check_jwt_token() fun me true yaa false hi likho
@app.middleware("http")
async def middleware(request: Request, call_next):

    start_time = datetime.utcnow()

    # modify request

    if not str(request.url).__contains__("/token"):

        try:
            jwt_token = request.headers["Authorization"].split("Bearer ")[1]
            # return Response(jwt_token)
            is_valid = check_jwt_token(jwt_token)
            #return Response(is_valid)
        except Exception as e:
            is_valid = False

        if not is_valid:
            return Response("You are not authorized", status_code=HTTP_401_UNAUTHORIZED)

    response = await call_next(request)

    # modify response
    execution_time = (datetime.utcnow() - start_time).microseconds
    response.headers["x-execution-time"] = str(execution_time)
    # Headers me key and value hmesh str me hi hoti hein (remember that)
    return response























