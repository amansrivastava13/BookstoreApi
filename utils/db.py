import asyncio
from utils.db_object import db
from utils.const import TESTING


# Create our execute function

async def execute(query, is_many, values=None):
    if TESTING:
        await db.connect()
    if is_many:
        await db.execute_many(query=query, values=values)
    else:
        await db.execute(query=query, values=values)
    if TESTING:
        await db.disconnect()


# Create your fetch function

async def fetch(query, is_one, values=None):
    if TESTING:
        await db.connect()
    if is_one:
        result = await db.fetch_one(query=query, values=values)
        if result is None:
            out = None
        else:
            out = dict(result)
    else:
        result = await db.fetch_all(query=query, values=values)
        if result is None:
            out = None
        else:
            out = []
            for row in result:
                out.append(dict(row))

    if TESTING:
        await db.disconnect()
    # print(out)
    return out

# query = "insert into books values(:isbn, :name, :author, :year)"
# values = {"isbn": "isbn1", "name": "book1", "author": "author1", "year": 2019}

# query = "insert into books values(:isbn, :name, :author, :year)"
# values = [{"isbn":"isbn2", "name":"book2","author":"author2", "year": 2020}, {"isbn":"isbn3", "name":"book3","author":"author3", "year": 2021}]

# query = "insert into books values(:isbn, :name, :author, :year)"
# values = {"isbn": "isbn5", "name": "book5", "author": "author5", "year": 2025}

# query = "select * from books where isbn = :isbn"
# values = {"isbn": "isbn1"}

# loop = asyncio.get_event_loop()
# loop.run_until_complete(execute(query,False,values))


# loop = asyncio.get_event_loop()
# loop.run_until_complete(fetch(query,False,values))

# query = "select * from books"

# loop = asyncio.get_event_loop()
# loop.run_until_complete(fetch(query,False))
