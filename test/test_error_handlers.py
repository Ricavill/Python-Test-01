from unittest.mock import patch

from starlette.testclient import TestClient

from test import set_secret_key, admin_user, admin_token, user_data,set_db_name


def test_validation_exception_handler(set_db_name):
    with patch("config.db.init_db", lambda: None):
        from main import app
        client = TestClient(app)
        with patch("config.error.logger.error") as mock_logger:
            response = client.post("/api/users/login",json={})  # Simulating a ValidationException being raised
            assert response.status_code == 400
            assert response.json() == {"message": "Email and password are required.", "error": True}
            mock_logger.assert_called()


def test_unauthorized_exception_handler(set_db_name):
    with patch("config.db.init_db", lambda: None):
        from main import app
        client = TestClient(app)
        with patch("config.error.logger.error"):
            response = client.get("/api/tweets/ingest")  # Simulating an UnauthorizedException being raised
            assert response.status_code == 401
            assert response.json() == {"detail": "Missing or invalid token"}


def test_not_found_exception_handler(set_db_name):
    with patch("config.db.init_db", lambda: None):
        from main import app
        client = TestClient(app)
        with patch("config.error.logger.error"):
            response = client.get("/not-found-route")  # Simulating a NotFoundException being raised
            assert response.status_code == 404
            assert response.json() == {"detail": "Not Found"}
