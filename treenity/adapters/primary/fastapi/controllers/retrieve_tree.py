"""Controller for retrieving a tree from the database."""

import dataclasses
import uuid

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from treenity.adapters.primary.fastapi.dependencies import get_branch_repository
from treenity.core.gateways.branch_repository import BranchRepository
from treenity.core.models.branch import Branch

router = APIRouter()


class GetTreeRequest(BaseModel):
    """Request model."""

    tree_id: str


@dataclasses.dataclass
class TreeData:
    """Store tree data."""

    id: str
    length: int
    children: list["TreeData"]


class GetTreeResponse(BaseModel):
    """Response model."""

    result: TreeData


@router.get("/trees/{tree_id}", response_model=GetTreeResponse, status_code=201)
async def get_tree_data(
    tree_id: str,
    branch_repository: BranchRepository = Depends(get_branch_repository),  # noqa: B008, `Depends` is a valid default
) -> GetTreeResponse:
    """Generate a new tree."""
    tree_root = branch_repository.get_by_id(uuid.UUID(tree_id))
    tree_data = _branch_to_dict(tree_root, branch_repository)

    return GetTreeResponse(result=tree_data)


def _branch_to_dict(branch: Branch, repository: BranchRepository) -> TreeData:
    """Convert branch to dictionary for JSON serialization."""
    children = []
    for child_id in branch.children_ids:
        child_branch = repository.get_by_id(child_id)
        children.append(_branch_to_dict(child_branch, repository))

    return TreeData(id=str(branch.id), length=branch.length, children=children)
