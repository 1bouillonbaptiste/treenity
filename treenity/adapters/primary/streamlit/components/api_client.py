"""API client for communicating with FastAPI backend."""

import requests

from treenity.adapters.primary.streamlit.components.models import TreeData, TreeID


class TreeAPIClient:
    """Client for tree generation API."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    def generate_tree(self, iterations: int) -> TreeID:
        """Generate a tree with specified iterations."""
        try:
            response: requests.Response = requests.post(
                f"{self.base_url}/generate-tree", json={"iterations": iterations}, timeout=5
            )
            response.raise_for_status()
            return TreeID(response.json()["result"])

        except requests.exceptions.ConnectionError:
            raise Exception(f"Cannot connect to FastAPI backend. Make sure it's running on {self.base_url}")  # noqa: B904
        except requests.exceptions.Timeout:
            raise Exception("Request timed out. Try reducing the number of iterations.")  # noqa: B904
        except requests.exceptions.HTTPError as e:
            if response.status_code == 400:
                error_detail = response.json().get("detail", "Bad request")
                raise Exception(f"Invalid input: {error_detail}")  # noqa: B904
            elif response.status_code == 500:
                error_detail = response.json().get("detail", "Server error")
                raise Exception(f"Server error: {error_detail}")  # noqa: B904
            else:
                raise Exception(f"HTTP {response.status_code}: {e!s}")  # noqa: B904
        except Exception as e:
            raise Exception(f"Unexpected error: {e!s}")  # noqa: B904

    def get_tree(self, tree_id: str) -> TreeData:
        """Get the current tree data for visualization."""
        try:
            response = requests.get(f"{self.base_url}/trees/{tree_id}", timeout=3)
            response.raise_for_status()
            return TreeData(**response.json()["result"])

        except requests.exceptions.ConnectionError:
            raise Exception("Cannot connect to FastAPI backend")  # noqa: B904
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                raise Exception(f"No tree data available for id {tree_id}. Generate a tree first.")  # noqa: B904
            else:
                error_detail = response.json().get("detail", str(e))
                raise Exception(f"Error getting tree data: {error_detail}")  # noqa: B904
        except Exception as e:
            raise Exception(f"Unexpected error: {e!s}")  # noqa: B904
