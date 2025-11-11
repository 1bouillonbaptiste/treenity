import pytest
from starlette.testclient import TestClient

from treenity.adapters.primary.fastapi.controllers import generate_tree, retrieve_tree


@pytest.fixture
def test_client():
    from fastapi import FastAPI

    app = FastAPI()
    app.include_router(generate_tree.router)
    app.include_router(retrieve_tree.router)

    return TestClient(app)
