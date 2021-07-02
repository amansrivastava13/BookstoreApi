from tests.all_tests import insert_user, clear_db, check_personel_user
from starlette.testclient import TestClient
from run import app

client = TestClient(app)


# Now our client is ready and we can send requests to our end points

def get_auth_header():
    insert_user("test", "test")
    response = client.post("/token", dict(username="test", password="test"))
    jwt_token = response.json()["access_token"]
    header = {"Authorization": f"Bearer {jwt_token}"}
    return header


def test_login_for_access_token():
    insert_user("user1", "pass1")
    response = client.post("/token", dict(username="user1", password="pass1"))
    # print(response.json())
    assert response.status_code == 200
    assert "access_token" in response.json()
    clear_db()


def test_login_for_access_token_unauthorized():
    insert_user("user1", "pass1")
    response = client.post("/token", dict(username="user2", password="pass2"))
    # print(response.json())
    assert response.status_code == 401
    clear_db()


# In this way we can increase the cases for our token end point


# Now create a test function for post /user
# It take a json in its body so import User first
def test_post_user():
    auth_header = get_auth_header()
    print(auth_header)
    user_dict = {"name": "user1", "password": "secret key", "mail": "a@b.com",
                 "role": "admin"}  # "name" ki jgh "username" likh doge toh error aaygi
    response = client.post("/v1/user", json=user_dict, headers=auth_header)
    print(response.json())
    assert response.status_code == 201
    assert check_personel_user("user1", "a@b.com") == True
    clear_db()


# lets create above function's one more case
def test_post_user_with_wrong_email():
    auth_header = get_auth_header()
    # print(auth_header)
    user_dict = {"name": "user1", "password": "secret key", "mail": "invalid",
                 "role": "admin"}  # "name" ki jgh "username" likh doge toh error aaygi
    response = client.post("/v1/user", json=user_dict, headers=auth_header)
    # print(response.json())
    assert response.status_code == 422
    clear_db()

# In this way we can create more test cases before uploading our code to production environment
