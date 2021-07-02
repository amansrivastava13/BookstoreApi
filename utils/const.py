# import os

JWT_SECRET_KEY = "9e4a7c7020769b8dab4aa38774bc57a454ecf739d62bf46d0ca77e053bbc5cbb"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_TIME_IN_MIN = 60 * 24 * 5

TOKEN_DESCRIPTION = "It verifies username and password from db and returns jwt token"
TOKEN_SUMMARY = "It returns jwt token"

DB_HOST = "localhost"
DB_USER = "aman"
DB_PASSWORD = "aman"
DB_NAME = "bookstore"
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

ISBN_DESCRIPTION = "It uniquely identifies the book"

UPLOA_PHOTO_APIKEY = "c723a27a576ac6c4368fd606d31d6660"
UPLOAD_PHOTO_URL = f"https://api.imgbb.com/1/upload?key={UPLOA_PHOTO_APIKEY}"

REDIS_URL = "redis://localhost"

TESTING = False

TEST_DB_HOST = "localhost"
TEST_DB_USER = "test"
TEST_DB_PASSWORD = "test"
TEST_DB_NAME = "test"
TEST_DB_URL = f"postgresql://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}/{TEST_DB_NAME}"

TEST_REDIS_URL = "redis://localhost"

IS_LOAD_TEST = False

DB_HOST_PRODUCTION = "68.183.92.221"
DB_URL_PRODUCTION = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST_PRODUCTION}/{DB_NAME}"
# IS_PRODUCTION = True if os.environ("PRODUCTION") == "true" else False
REDIS_URL_PRODUCTION = "redis://68.183.92.221"

JWT_EXPIRED_MSG = "Your jwt token is expired ! Renew thw jwt token !"
JWT_INVALID_MSG = "Invalid jwt token !"
TOKEN_INVALID_CREDENTIALS_MSG = "You can't access with these credentials. Invalid username or password !"
JWT_WRONG_ROLE = "Unauthorized role"

THIS_USERNAME_DO_NOT_EXIST = "This username do not exist in database"
