from pydantic import BaseModel
from fastapi import Query
import enum


class Role(str, enum.Enum):
    admin = "admin"
    personel = "personel"


class User(BaseModel):
    name: str = "default"
    password: str
    mail: str = Query(..., regex="^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$")
    role: Role
