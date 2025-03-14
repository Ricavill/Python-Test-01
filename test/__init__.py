import datetime
import os

import pytest

from user.model import User


@pytest.fixture
def set_db_name(monkeypatch):
    monkeypatch.setenv("JELOU_DB_FILE", "sqlite:///jelou.db")


@pytest.fixture
def admin_user():
    date_str = "2025-03-14 01:37:46.502373"
    dt_object = datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
    return User(id=1, email='ric@hotmail.com',
                pass_hash="243262243132243930615651584436787175716f2f3874715372542e4f4d634a48504d68616b55696"
                          "e473779386e4b77714f5567614a42434f717479", created_at=dt_object
                )


@pytest.fixture
def admin_token():
    return ('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwibmFtZSI6bnVsbCwiZW1haWwiOiJyaWNAaG90bWFpbC5jb20iLCJjcmVhd'
            'GVkX2F0IjoiMjAyNS0wMy0xNFQwMTozNzo0Ni41MDIzNzMiLCJleHAiOjI3NjYxOTAxNTEzfQ.LttF5bp1gSIAhihxMjCtZ8AzVuQE'
            '-MmxY-NHdIm8kqw')


@pytest.fixture
def user_data():
    return {"name": "ric", "email": "ric@hotmail.com", "password": "ric123"}


@pytest.fixture
def set_secret_key(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "jelouAI")
