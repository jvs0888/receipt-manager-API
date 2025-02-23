import httpx
import pytest
from fastapi.testclient import TestClient


@pytest.mark.order(5)
def test_get_receipt_list(client: TestClient, login: str) -> None:
    response: httpx.Response = client.get(url="/receipt/1")
    assert response.status_code == 200
    assert "Дякуємо за покупку!" in response.text
