"""Tree generator using FastAPI."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from treenity.adapters.primary.fastapi.controllers import grow_tree_controller
from treenity.adapters.secondary.gateways.dual_split_strategy import DualSplitStrategy
from treenity.adapters.secondary.gateways.in_memory_branch_repository import InMemoryBranchRepository
from treenity.core.grow_tree import GrowTreeUseCase


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager."""
    # Wiring
    branch_repository = InMemoryBranchRepository()
    split_strategy = DualSplitStrategy(split_probability=0.1)
    grow_tree_use_case = GrowTreeUseCase(
        branch_repository=branch_repository,
        split_strategy=split_strategy,
    )

    app.state.branch_repository = branch_repository
    app.state.split_strategy = split_strategy
    app.state.grow_tree_use_case = grow_tree_use_case

    yield


app = FastAPI(title="Tree Generator", version="1.0.0", lifespan=lifespan)
app.include_router(grow_tree_controller.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)  # noqa: S104
