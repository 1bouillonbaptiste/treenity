"""Implements `BranchRepository` with in-memory storage."""

import dataclasses

from treenity.core.gateways.branch_repository import BranchRepository
from treenity.core.models.branch import Branch


@dataclasses.dataclass
class InMemoryBranchRepository(BranchRepository):
    """In memory branch repository."""

    def __init__(self):
        self.branches: list[Branch] = []

    def save(self, branch: Branch) -> None:
        """Save a branch in memory."""
        self.branches.append(branch)
