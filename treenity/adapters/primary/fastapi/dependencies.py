"""Application runtime dependencies."""

from fastapi import Depends
from starlette.requests import Request

from treenity.core.gateways.branch_repository import BranchRepository
from treenity.core.gateways.split_strategy import SplitStrategy
from treenity.core.grow_tree import GrowTreeUseCase


def get_branch_repository(request: Request) -> BranchRepository:
    """Get the in-memory branch repository."""
    return request.app.state.branch_repository


def get_split_strategy(request: Request) -> SplitStrategy:
    """Get the dual split strategy."""
    return request.app.state.split_strategy


def get_grow_tree_use_case(
    branch_repository: BranchRepository = Depends(get_branch_repository),  # noqa: B008, `Depends` is a valid default
    split_strategy: SplitStrategy = Depends(get_split_strategy),  # noqa: B008, `Depends` is a valid default
) -> GrowTreeUseCase:
    """Get the grow tree use case."""
    return GrowTreeUseCase(
        branch_repository=branch_repository,
        split_strategy=split_strategy,
    )
