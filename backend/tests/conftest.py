import pytest
from fastapi.testclient import TestClient

from app import main


@pytest.fixture(autouse=True)
def reset_db():
    main.db["notes"].clear()
    main.db["next_id"] = 1


@pytest.fixture
def client():
    return TestClient(main.app)