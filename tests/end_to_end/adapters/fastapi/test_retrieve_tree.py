from uuid import UUID

from starlette.testclient import TestClient

from treenity.adapters.primary.fastapi.controllers.retrieve_tree import GetTreeResponse, TreeData
from treenity.adapters.primary.fastapi.dependencies import get_branch_repository
from treenity.adapters.secondary.gateways.in_memory_branch_repository import InMemoryBranchRepository
from treenity.core.models.branch import Branch


def test_can_retrieve_an_existing_tree_with_branches(test_client: TestClient):
    branch_repository = InMemoryBranchRepository()
    branch_repository.save(
        branch=Branch(
            id=UUID("1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3"),
            length=1,
            children_ids=[UUID("dcf8b64a-dac7-4644-b89f-040b2d07457f"), UUID("33e8ec10-acc5-49ec-a716-958ddb9bf9c5")],
        )
    )
    branch_repository.save(branch=Branch(id=UUID("dcf8b64a-dac7-4644-b89f-040b2d07457f"), length=1))
    branch_repository.save(branch=Branch(id=UUID("33e8ec10-acc5-49ec-a716-958ddb9bf9c5"), length=1))

    test_client.app.dependency_overrides[get_branch_repository] = lambda: branch_repository

    response = test_client.get("/trees/1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3")

    assert response.status_code == 201, response.text

    client_response = GetTreeResponse.model_validate(response.json())
    assert client_response.result == TreeData(
        id="1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3",
        length=1,
        children=[
            TreeData(id="dcf8b64a-dac7-4644-b89f-040b2d07457f", length=1, children=[]),
            TreeData(id="33e8ec10-acc5-49ec-a716-958ddb9bf9c5", length=1, children=[]),
        ],
    )
