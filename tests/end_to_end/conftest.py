import pytest
from starlette.testclient import TestClient

from treenity.adapters.primary.fastapi.controllers import grow_tree_controller


@pytest.fixture
def test_client():
    from fastapi import FastAPI

    app = FastAPI()
    app.include_router(grow_tree_controller.router)

    return TestClient(app)
