from fastapi import FastAPI, Body, Header, File, Depends,HTTPException
from models.user import User
from models.author import Author
from models.book import Book
from starlette.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from starlette.responses import Response
from fastapi.security import OAuth2PasswordRequestForm
from utils.security import authenticate_user, create_jwt_token
from models.jwt_user import JWTUser

app_v1 = FastAPI(openapi_prefix='/v1') #First step of versioning
# oauth_schema = OAuth2PasswordBearer(tokenUrl="/token") (yeh security.py me define hoga)

@app_v1.get("/hello")
async def my_first_api():
    return {"Congrats! Finally you have your own response in Postman"}

@app_v1.post("/user", status_code=HTTP_201_CREATED)
async def post_user(user:User, x_custom_key: str = Header(...)):
    return {"Request Body is": user, "request Header is":x_custom_key}    # colon(:) "" iske andr aayaga toh error aa jaygi & always use snake cases while declaring variables in python

@app_v1.get("/user")
async def get_user_validation(password:str):
    return {"query parammeter": password}

@app_v1.get("/book/{isbn}")
async def get_book_with_isbn(isbn:str):
    return {"pet parameter":isbn}

@app_v1.get("/author/{id}/book")
async def get_authors_books(id:int, category: str, order: str = "asc"):
    return {"Query parameter":str(id)+category+order}

@app_v1.patch("/author/name")
async def patch_author_name(name: str = Body(..., embed= True)):
    return {"name in body": name}

@app_v1.post("/user/author")
async def post_user_and_author(user:User,author:Author,bookstore_name: str = Body(...,embed=True)):       # we can't user hyphen(-) while giving name of parameters
    return{"user":user, "author":author, "name of bookstore":bookstore_name}

# Now we want header from our users (see request 2)

# How to return model in get response (by returning object of response model class)
@app_v1.get("/book", response_model=Book, response_model_exclude=["author","name"])
async def get_response_model():
    author_dict={
        "name":"author1",
        "book": ["book2", "book3", "book4", "book5"]
    }
    author_obj = Author(**author_dict)
    book_dict={
        "isbn":"isbn1",
        "name":"book1",
        "year": 2021,
        "author":author_obj
    }
    book_obj = Book(**book_dict)
    #return {"response model": book_obj} (this gives response ISE)
    return book_obj

# How to return our own status code (see req 2)

#How to get multipart form (in File)
@app_v1.post("/user/photo")
async def upload_user_photo(profile_photo: bytes = File(...)):
    return {"file size":len(profile_photo)}

#How to get response in response header (rem that value of all headers is string only)
@app_v1.post("/user/photo/api")
async def upload_user_photo(response:Response, profile_photo: bytes = File(...)):
    response.headers["x-file-size"] = str(len(profile_photo))
    response.set_cookie(key="my-cookie-api", value=124)
    return {"file size":len(profile_photo)}

@app_v1.put("/update")
async def my_post_api(book: str = Body(...,embed=True)):
    return {"your updated key is":book}

# async def my_post_api(book: str = Body("default",embed=True))
# async def my_post_api(book: str = Body(None,embed=True))

@app_v1.delete("/delete")
async def value_to_be_deleted(del_value: str):
    return {"This value should be deleted from DB": del_value}



# form url encoded
@app_v1.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    jwt_user_dict_2 = {
        "username": form_data.username,
        "password":form_data.password
    }
    object = JWTUser(**jwt_user_dict_2)

    user = authenticate_user(object)
    if user is None:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    jwt_token_2 = create_jwt_token(user)
    return {"token": jwt_token_2}

