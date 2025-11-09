"""Application runtime dependencies."""

from fastapi import Depends
from starlette.requests import Request

from treenity.adapters.secondary.gateways.dual_split_strategy import DualSplitStrategy
from treenity.adapters.secondary.gateways.in_memory_branch_repository import InMemoryBranchRepository
from treenity.core.grow_tree import GrowTreeUseCase


def get_branch_repository(request: Request) -> InMemoryBranchRepository:
    """Get the in-memory branch repository."""
    return request.app.state.branch_repository


def get_split_strategy(request: Request) -> DualSplitStrategy:
    """Get the dual split strategy."""
    return request.app.state.split_strategy


def get_grow_tree_use_case(
    branch_repository: InMemoryBranchRepository = Depends(get_branch_repository),  # noqa: B008, `Depends` is a valid default
    split_strategy: DualSplitStrategy = Depends(get_split_strategy),  # noqa: B008, `Depends` is a valid default
) -> GrowTreeUseCase:
    """Get the grow tree use case."""
    return GrowTreeUseCase(
        branch_repository=branch_repository,
        split_strategy=split_strategy,
    )
