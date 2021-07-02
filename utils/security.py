from passlib.context import CryptContext
from models.jwt_user import JWTUser
from datetime import datetime, timedelta
from utils.const import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRATION_TIME_IN_MIN, JWT_EXPIRED_MSG, JWT_INVALID_MSG, \
    JWT_WRONG_ROLE, THIS_USERNAME_DO_NOT_EXIST
import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
import time
from utils.db_functions import db_check_username_and_password_for_authentication, db_check_jwt_username

pwd_context = CryptContext(schemes=["bcrypt"])
oauth_schema = OAuth2PasswordBearer(tokenUrl="/token")


# jwt_user_dict = {
#     "username": "user1",
#     "password": "$2b$12$1bD/n3s6ypBd14ZJKzXm.Ovq/BN7O7dRXvaEvVF4i2Z8TLvp7zdpi"
# }
# jwt_user_obj = JWTUser(**jwt_user_dict)
# Ignore above lines


def get_hashed_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        return False


# print(get_hashed_password("aman"))
# hashed = get_hashed_password("aman")
# print(verify_password("ama",hashed))
# print(get_hashed_password("secretkey"))

# Authenticate username and password to give jwt token
async def authenticate_user(user: JWTUser):
    potential_users = await db_check_username_and_password_for_authentication(user)
    is_valid = False
    for db_user in potential_users:
        if verify_password(user.password, db_user["password"]):
            is_valid = True

    if is_valid is True:
        user.role = "admin"
        return user

    return None


# Create Access JWT token
def create_jwt_token(user: JWTUser):
    expiration = datetime.utcnow() + timedelta(JWT_EXPIRATION_TIME_IN_MIN)
    jwt_payload = {
        "sub": user.username,
        "role": user.role,
        "exp": expiration,
    }
    jwt_token = jwt.encode(jwt_payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return jwt_token


# Check whether jwt token is correct or not
async def check_jwt_token(token: str = Depends(oauth_schema)):
    try:
        jwt_paylaod = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        username = jwt_paylaod.get("sub")
        role = jwt_paylaod.get("role")
        expiration = jwt_paylaod.get("exp")
        if time.time() < expiration:
            is_valid = await db_check_jwt_username(username)
            if is_valid:
                final_checks(role)
            else:
                raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=JWT_INVALID_MSG)
        else:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=JWT_EXPIRED_MSG)

        # return True
    except Exception as e:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=JWT_WRONG_ROLE)


# Last checking and returning the final result
def final_checks(role: str):
    if role == "admin":
        return True
    else:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

# print(check_jwt_token("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyMSIsInJvbGUiOiJhZG1pbiIsImV4cCI6MjI0MzcwNjIyNX0.p8vEj5aq5Zbpj_bDrTFJRlqQLXDN6VeQvQZL8MDtxOA"))
# sahi token pass krane pe None aa rha hey (Ab jb hmne line 65 pe return True mention kia hey toh yeh ab sahi True/False return kr raha hey) &
# wrong token pass krane pe False aa rha hey

# print(get_hashed_password('secret'))

# print(get_hashed_password('test'))
