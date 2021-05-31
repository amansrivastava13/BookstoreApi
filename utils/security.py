from passlib.context import CryptContext
from models.jwt_user import JWTUser
from datetime import datetime, timedelta
from utils.const import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRATION_TIME_IN_MIN
import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED
import time

pwd_context = CryptContext(schemes=["bcrypt"])
oauth_schema = OAuth2PasswordBearer(tokenUrl="/token")

jwt_user_dict = {
    "username": "user1",
    "password": "$2b$12$1bD/n3s6ypBd14ZJKzXm.Ovq/BN7O7dRXvaEvVF4i2Z8TLvp7zdpi"
}
jwt_user_obj = JWTUser(**jwt_user_dict)

def get_hashed_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password:str, hashed_password:str):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        return False

# print(get_hashed_password("aman"))
# hashed = get_hashed_password("aman")
# print(verify_password("ama",hashed))
# print(get_hashed_password("secretkey"))

# Authenticate username and password to give jwt token
def authenticate_user(user:JWTUser):
    if jwt_user_obj.username == user.username:
        if verify_password(user.password, jwt_user_obj.password):
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
    jwt_token = jwt.encode(jwt_payload, JWT_SECRET_KEY, algorithm= JWT_ALGORITHM)
    return jwt_token

#Check whether jwt token is correct or not
def check_jwt_token(token:str = Depends(oauth_schema)):
    try:
        jwt_paylaod = jwt.decode(token, JWT_SECRET_KEY, algorithms= JWT_ALGORITHM)
        username = jwt_paylaod.get("sub")
        role = jwt_paylaod.get("role")
        expiration = jwt_paylaod.get("exp")

        if time.time() < expiration:
            if jwt_user_obj.username == username:
                final_checks(role)

        return True
    except Exception as e:
        return False

     #raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)


# Last checking and returning the final result
def final_checks(role:str):
    if role == "admin":
        return True
    else:
        return False
    

#print(check_jwt_token("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyMSIsInJvbGUiOiJhZG1pbiIsImV4cCI6MjI0MzcwNjIyNX0.p8vEj5aq5Zbpj_bDrTFJRlqQLXDN6VeQvQZL8MDtxOA"))
# sahi token pass krane pe None aa rha hey (Ab jb hmne line 65 pe return True mention kia hey toh yeh ab sahi True/False return kr raha hey) &
# wrong token pass krane pe False aa rha hey