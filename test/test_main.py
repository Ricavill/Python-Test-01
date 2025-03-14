from unittest.mock import patch

import pandas as pd
from starlette.testclient import TestClient

from test import set_secret_key, admin_user, admin_token, user_data,set_db_name
from tweet.tweet_repository import TweetRepository
from user.user_repository import UserRepository


def test_read_root(set_db_name):
    with patch("config.db.init_db", lambda: None):
        from main import app
        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"Hello": "World"}


def test_openapi_json(set_db_name):
    with patch("config.db.init_db", lambda: None):
        from main import app
        client = TestClient(app)
        response = client.get("/api/v1/openapi.json")
        assert response.status_code == 200


def test_docs(set_db_name):
    with patch("config.db.init_db", lambda: None):
        from main import app
        client = TestClient(app)
        response = client.get("/documentation")
        assert response.status_code == 200


def test_users_router(admin_user, set_db_name):
    with patch("config.db.init_db", lambda: None), patch.object(UserRepository, "get_by_email",
                                                                return_value=admin_user):
        from main import app
        client = TestClient(app)
        response = client.post("/api/users/login",
                               json={"email": "ric@hotmail.com", "password": "ric123"})  # Assuming this endpoint exists
        assert response.status_code in [200, 401]  # Depending on auth middleware


def test_tweets_router(set_db_name):
    with patch("config.db.init_db", lambda: None):
        from main import app
        client = TestClient(app)
        response = client.get("/api/tweets/ingest")  # Assuming this endpoint exists
        assert response.status_code in [200, 401]


def test_companies_router(set_db_name):
    with patch("config.db.init_db", lambda: None), \
            patch.object(TweetRepository, "get_all", return_value=pd.DataFrame({"inbound": [1]})), \
            patch.object(TweetRepository, "get_tweet_response_rate", return_value=0), \
            patch.object(TweetRepository, "get_conversation_ratio", return_value=0), \
            patch.object(TweetRepository, "get_volume_metrics", return_value=0), \
            patch.object(TweetRepository, "get_avg_response_time", return_value=0):
        from main import app
        client = TestClient(app)
        response = client.get("/api/companies/hola/insights")  # Assuming this endpoint exists
        assert response.status_code in [200, 401]
