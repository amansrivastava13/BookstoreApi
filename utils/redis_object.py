import aioredis
from utils.const import TESTING, TEST_REDIS_URL

# Create a redis object and assign it to None
redis = None


# Create a fun so that when we are in testing mode we use test redis and not real redis
async def check_test_redis():
    global redis
    if TESTING:
        redis = await aioredis.create_redis_pool(TEST_REDIS_URL)
