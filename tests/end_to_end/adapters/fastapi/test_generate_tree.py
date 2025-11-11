import uuid

from starlette.testclient import TestClient

from treenity.adapters.primary.fastapi.controllers.generate_tree import GenerateTreeResponse
from treenity.adapters.primary.fastapi.dependencies import get_branch_repository, get_split_strategy
from treenity.adapters.secondary.gateways.dual_split_strategy import DualSplitStrategy
from treenity.adapters.secondary.gateways.in_memory_branch_repository import InMemoryBranchRepository
from treenity.core.models.branch import Branch


def test_can_grow_a_new_tree(test_client: TestClient):
    branch_repository = InMemoryBranchRepository()
    split_strategy = DualSplitStrategy(split_probability=0.0)

    test_client.app.dependency_overrides[get_branch_repository] = lambda: branch_repository
    test_client.app.dependency_overrides[get_split_strategy] = lambda: split_strategy

    response = test_client.post("/generate-tree", json={"iterations": 1})

    assert response.status_code == 201

    client_response = GenerateTreeResponse.model_validate(response.json())
    assert branch_repository.get_by_id(uuid.UUID(client_response.result)) == Branch(
        id=uuid.UUID(client_response.result), length=2
    )


def test_can_grow_a_new_tree_with_branches(test_client: TestClient):
    branch_repository = InMemoryBranchRepository()
    split_strategy = DualSplitStrategy(split_probability=1.0)

    test_client.app.dependency_overrides[get_branch_repository] = lambda: branch_repository
    test_client.app.dependency_overrides[get_split_strategy] = lambda: split_strategy

    response = test_client.post("/generate-tree", json={"iterations": 6})

    assert response.status_code == 201

    client_response = GenerateTreeResponse.model_validate(response.json())

    result_tree = branch_repository.get_by_id(uuid.UUID(client_response.result))

    assert result_tree.id == uuid.UUID(client_response.result)
    assert result_tree.length == 6
    assert len(result_tree.children_ids) == 2
