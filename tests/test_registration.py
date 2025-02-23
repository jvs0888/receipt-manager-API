import pytest
from fastapi.testclient import TestClient


@pytest.mark.order(1)
def test_registration(client: TestClient, register: tuple) -> None:
    username, password = register
    assert username
    assert password
