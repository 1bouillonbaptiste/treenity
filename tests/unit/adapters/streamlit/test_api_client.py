from unittest.mock import Mock, patch

import pytest

from treenity.adapters.primary.streamlit.components.api_client import TreeAPIClient, TreeID
from treenity.adapters.primary.streamlit.components.models import TreeData


@pytest.fixture
def api_client():
    return TreeAPIClient(base_url="http://fake-server:8000")


@patch("requests.post")
def test_can_generate_a_tree(mock_post: Mock, api_client: TreeAPIClient):
    # Given
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": "123e4567-e89b-12d3-a456-426614174000"}
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    # When
    result = api_client.generate_tree(iterations=1)

    # Then
    assert result == TreeID("123e4567-e89b-12d3-a456-426614174000")


@patch("requests.get")
def test_can_retrieve_a_tree(mock_get: Mock, api_client: TreeAPIClient):
    # Given
    tree_data = {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "length": 5,
        "children": [{"id": "987fcdeb-51a2-43d1-9f4e-123456789abc", "length": 3, "children": []}],
    }
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": tree_data}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    # When
    result = api_client.get_tree("123e4567-e89b-12d3-a456-426614174000")

    # Then
    assert result.id == "123e4567-e89b-12d3-a456-426614174000"
    assert result.length == 5
    assert len(result.children) == 1
    assert result.children[0] == TreeData(
        id="987fcdeb-51a2-43d1-9f4e-123456789abc",
        length=3,
        children=[],
    )
