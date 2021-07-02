**BookStore:**

**
Project Description**

Developed backend architecture for a bookstore. For developing APIs, fastapi python framework is used
Perform development, testing and finally then released on cloud
APIs are secure, fast, scalable, cached, versioned, tested and well documented
For faster response, caching is done using redis
Postgres is used for database
Used docker as a deployment mechanism
load balacer is used for handling large number of users
Before deployment on cloud, tested the whole code. Testing includes System Testing using Pytest and Load Testing which was done using locust and apache bench
Tech Stack: Python, FastApi Python Framework, Redis, Postgres, Docker, Nginx

**
Command to run the code:**
1. Move inside your venv, using cmd: source venv/bin/activate
2. Run code using: uvicorn run:app --reload --port 3000

**Libraries used:**
1. aioredis
2. asyncpg
4. bcrypt- for authentication
5. black
6. databases
7. fastapi
8. flask8
9. PyJWT- for authentication using jwt token
10. locust- for load testing
11. passlib
12. pydantic
13. pytest- for unit testing
14. python-multipart
15. requests
16. schema
17. SQLAlchemy- For database
18. starlette
19. uvicorn

IDE used: Pycharm

This code is Deployed on Digital Ocean's Droplets

