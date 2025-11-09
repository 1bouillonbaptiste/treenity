"""Implements `BranchRepository` with in-memory storage."""

import dataclasses
import uuid

from treenity.core.gateways.branch_repository import BranchRepository
from treenity.core.models.branch import Branch


@dataclasses.dataclass
class InMemoryBranchRepository(BranchRepository):
    """In memory branch repository."""

    def __init__(self):
        self.branches: dict[uuid.UUID, Branch] = {}

    def save(self, branch: Branch) -> None:
        """Save a branch in memory."""
        self.branches[branch.id] = branch

    def has_id(self, branch_id: uuid.UUID) -> bool:
        """Check if the branch exists."""
        return branch_id in self.branches

    def get_by_id(self, branch_id: uuid.UUID) -> Branch:
        """Retrieve a branch from the repository."""
        return self.branches[branch_id]
