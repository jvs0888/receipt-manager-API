import random
from pathlib import Path

import pytest
import httpx
from fastapi.testclient import TestClient

try:
    from app.main import init_app
except ImportError as ie:
    exit(f'{ie} :: {Path(__file__).resolve()}')


@pytest.fixture(scope="session")
def client() -> TestClient:
    with TestClient(app=init_app()) as client:
        yield client

@pytest.fixture(scope="session")
def register(client: TestClient) -> tuple:
    username: str = f"TEST_USER_{random.randint(100, 1000)}"
    password: str = "TEST_PASSWORD"

    payload: dict = {
        "name": "TEST_NAME",
        "username": username,
        "password": password
    }

    response: httpx.Response = client.post(url="/register", json=payload)
    assert response.status_code == 201

    return username, password

@pytest.fixture(scope="session")
def login(client: TestClient, register: tuple) -> str:
    username, password = register

    payload: dict = {
        "username": username,
        "password": password
    }

    response: httpx.Response = client.post(url="/login", json=payload)
    assert response.status_code == 200

    token = response.json().get("token")
    assert token

    return token
