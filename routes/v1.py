from fastapi import FastAPI, Body, Header, File, Depends, HTTPException, APIRouter
from models.user import User
from models.author import Author
from models.book import Book
from starlette.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from starlette.responses import Response
from utils.db_functions import (db_insert_persnoel, db_check_personel, db_get_book_with_isbn, db_get_author,
                                db_get_author_from_id,
                                db_patch_author_name)
from utils.helper_functions import upload_img_to_server
import utils.redis_object as re
import pickle

app_v1 = APIRouter()  # First step of versioning


# oauth_schema = OAuth2PasswordBearer(tokenUrl="/token") (yeh security.py me define hoga)

@app_v1.get("/hello")
async def my_first_api():
    return {"Congrats! Finally you have your own response in Postman"}


@app_v1.post("/user", status_code=HTTP_201_CREATED, tags=["User"])
async def post_user(user: User):  # Insert this user in users table in the database
    await db_insert_persnoel(user)
    return {"result": "persnoel is created"}  # colon(:) "" iske andr aayaga toh error aa jaygi & always use snake cases while declaring variables in python


@app_v1.post("/login")
async def get_user_validation(username: str = Body(...), password: str = Body(
    ...)):  # We have to check if this username and password is in personel table or not

    # first ask to redis instead going to database (so first import redis_object)
    redis_key = f"{username},{password}"
    result = await re.redis.get(redis_key)

    # Redis has the data
    if result:
        #print(result) # This is how we debug the code
        if result == b'True':  # redis ki values kabhi boolean me store nhi hoti so hmne true ar false as a string maana hey
            return {"is_valid (coming from redis 1)": True}
        else:
            return {"is_valid (coming from redis 2)": False}

    # Redis does not have the data
    else:
        # Once fetch the result from the database if redis does not have the data And then save it to the redis a key and value
        result = await db_check_personel(username, password)

        # Now above function returns True or False But in redis we cannot store boolean values. We can store any type of value like int, float but not boolean
        await re.redis.set(redis_key, str(result), expire = 10)


        return {"is_valid (coming from db)": result}


@app_v1.get("/book/{isbn}", tags=["Books"])
async def get_book_with_isbn(isbn: str):  # get book from the books table having this isbn
    result = await db_get_book_with_isbn(isbn)
    return {"pet parameter": result}


@app_v1.get("/author/{id}/book", tags=["Books"])  # get all the books of this specific author
async def get_authors_books(id: int, order: str = "asc"):
    author = await db_get_author_from_id(id)
    if author is not None:
        books = author["book"]
        if order == "asc":
            books = sorted(books)
        else:
            books = sorted(books, reverse=True)
        return {"books": books}

    else:
        return {"result": "No author with corresponding id"}


@app_v1.patch("/author/{id}/name")
async def patch_author_name(id: int, name: str = Body(..., embed=True)):  # It updates the author's name
    await db_patch_author_name(id, name)
    return {"result": "name is updated"}


@app_v1.post("/user/author", tags=["User"])  # It is not a logical point
async def post_user_and_author(user: User, author: Author, bookstore_name: str = Body(...,
                                                                                      embed=True)):  # we can't user hyphen(-) while giving name of parameters
    return {"user": user, "author": author, "name of bookstore": bookstore_name}


# Now we want header from our users (see request 2)

# How to return model in get response (by returning object of response model class)

# This functions run only when: suppose for isbn1 books table me author hey author1 so authors table me author1 naam hone hi chahiye wrna 500 de dega
@app_v1.get("/test/book/{isbn}", response_model=Book) #response_model_exclude=["author", "name"]
async def get_response_model(isbn: str):

    result = await re.redis.get(isbn)
    if result:
        result_book = pickle.loads(result)
        return result_book

    else:
        book = await db_get_book_with_isbn(isbn)
        author = await db_get_author(book["author"])
        author_obj = Author(**author)  # ModelMetaclass object argument after ** must be a mapping, not NoneType
        book["author"] = author_obj
        result_book = Book(**book)

        await re.redis.set(isbn, pickle.dumps(result_book)) # redis cannot store objects. So for store objects in redis we have to first convert it in bytes using pickle library
        return result_book


# How to return our own status code (see req 2)

# How to get multipart form (in File)
# We can't store images in postgres so one idea is we can try to upload the image from users to a image server (here we use api.imgbb.com) and store that url in our database
@app_v1.post("/user/photo")
async def upload_user_photo(profile_photo: bytes = File(...)):
    await upload_img_to_server(profile_photo)
    return {"file size": len(profile_photo)}


# How to get response in response header (rem that value of all headers is string only)
# ************************************ Learning Purpose ***************************************************************
@app_v1.post("/user/photo/api")
async def upload_user_photo(response: Response, profile_photo: bytes = File(...)):
    response.headers["x-file-size"] = str(len(profile_photo))
    response.set_cookie(key="my-cookie-api", value=124)
    return {"file size": len(profile_photo)}


@app_v1.put("/update")
async def my_post_api(book: str = Body(..., embed=True)):
    return {"your updated key is": book}


# async def my_post_api(book: str = Body("default",embed=True))
# async def my_post_api(book: str = Body(None,embed=True))

@app_v1.delete("/delete")
async def value_to_be_deleted(del_value: str):
    return {"This value should be deleted from DB": del_value}
