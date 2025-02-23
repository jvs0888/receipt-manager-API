import httpx
import pytest
from fastapi.testclient import TestClient


@pytest.mark.order(3)
def test_create_receipt(client: TestClient, login: str) -> None:
    headers: dict = {
        "Authorization": f"Bearer {login}"
    }

    payload: dict = {
        "products": [
            {
                "name": 'TEST_Apple',
                "price": 121.56,
                "quantity": 4,
            },
            {
                "name": 'TEST_Orange',
                "price": 199.99,
                "quantity": 2,
            }
        ],
        "payment": {
            "type": "cash",
            "amount": 1500,
        }
    }

    response: httpx.Response = client.post(url="/receipt/create", headers=headers, json=payload)
    assert response.status_code == 201
