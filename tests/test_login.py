import pytest
from fastapi.testclient import TestClient


@pytest.mark.order(2)
def test_login(client: TestClient, login: str) -> None:
    token: str = login
    assert token
