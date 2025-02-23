import httpx
import pytest
from fastapi.testclient import TestClient


@pytest.mark.order(4)
def test_get_receipt_list(client: TestClient, login: str) -> None:
    headers: dict = {
        "Authorization": f"Bearer {login}"
    }

    response: httpx.Response = client.get(url="/receipt/list", headers=headers)
    assert response.status_code == 200
