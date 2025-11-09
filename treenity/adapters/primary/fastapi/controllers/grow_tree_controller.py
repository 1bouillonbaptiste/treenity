"""Controller for `GrowTreeUseCase`."""

import uuid

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from treenity.adapters.primary.fastapi.dependencies import get_grow_tree_use_case
from treenity.core.grow_tree import GrowTreeUseCase

router = APIRouter()


class GenerateTreeRequest(BaseModel):
    """Request model."""

    iterations: int = Field(default=10, ge=1, le=50)


class GenerateTreeResponse(BaseModel):
    """Response model."""

    result: str


@router.post("/generate-tree", response_model=GenerateTreeResponse, status_code=201)
async def generate_tree(
    request: GenerateTreeRequest,
    grow_tree_use_case: GrowTreeUseCase = Depends(get_grow_tree_use_case),  # noqa: B008, `Depends` is a valid default
):
    """Generate a new tree."""
    new_tree_id = uuid.uuid4()
    grow_tree_use_case.execute(tree_id=new_tree_id, iterations=request.iterations)

    return GenerateTreeResponse(result=str(new_tree_id))
