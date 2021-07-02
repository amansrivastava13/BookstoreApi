from utils.db import fetch, execute
import asyncio  # To use async fun like execute and fetch inside sync function. Remember that testclient is a sync function
from utils.security import get_hashed_password

loop = asyncio.get_event_loop()


def insert_user(usename, password):  # mail and role can be None. This function inserts user to our test database
    query = """insert into users(username, password) values(:username, :password)"""
    hashed_password = get_hashed_password(password)
    values = {"username": usename, "password": hashed_password}
    loop.run_until_complete(execute(query, False, values))  # see ki hmne execute fun ke pehle await nhi lgaya hey


def check_personel_user(username, mail):
    query = """select * from personel where username = :username and mail = :mail"""
    values = {"username": username, "mail": mail}
    result = loop.run_until_complete(fetch(query, True, values))
    if result is None:
        return False
    return True



def clear_db():
    query1 = """delete from users"""
    query2 = """delete from authors"""
    query3 = """delete from books"""
    query4 = """delete from personel"""

    loop.run_until_complete(execute(query1, False))
    loop.run_until_complete(execute(query2, False))
    loop.run_until_complete(execute(query3, False))
    loop.run_until_complete(execute(query4, False))

# Lets create our first test function (pytest)
# Rem that all pytest function name should start with test_ otherwise it will not work
