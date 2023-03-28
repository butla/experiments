from fastapi.testclient import TestClient
import pytest

from sample_backend.main import app


@pytest.fixture
def test_client():
    return TestClient(app)


def test_hello_endpoint(test_client: TestClient):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"hello": "world"}
