from databases import Database
from utils.const import DB_URL, TESTING, TEST_DB_URL, IS_LOAD_TEST, DB_URL_PRODUCTION

# from utils.const import IS_PRODUCTION

if TESTING or IS_LOAD_TEST:
    db = Database(TEST_DB_URL)

# elif IS_PRODUCTION:
#    db = Database(DB_URL_PRODUCTION)

else:
    db = Database(DB_URL)

# We need to connect this db object when api starts and we need to disconnect this db object when api stops
