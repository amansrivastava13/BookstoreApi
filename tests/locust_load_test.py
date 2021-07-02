from locust import HttpUser, task


class BookstoreLoadTest(HttpUser):
    # @task
    # def token_test(self):
    #     self.client.post("/token", dict(username="test", password="test"))

    @task
    def test_post_user(self):
        user_dict = {"name": "personel1", "password": "pass1", "role": "admin", "mail": "a@b.com"}
        auth_header = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyMSIsInJvbGUiOiJhZG1pbiIsImV4cCI6MjI0NjI1NjI3MH0.Dm41SDtJ1AsqNnZLxIKNa7fh2nCBex0MZg6e5T1r668"}
        self.client.post("/v1/user", json=user_dict, headers=auth_header)

    host = "http://localhost:3000"  # must parameter

    # Now we can load test the token api
    # min_wait = 5000  # ie 5 sec    optional parameter
    # max_wait = 9000  # ie 9 sec    optional parameter
