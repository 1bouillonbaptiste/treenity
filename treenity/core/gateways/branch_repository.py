"""Interface for branch repository."""

import dataclasses
import uuid
from typing import Protocol

from treenity.core.models.branch import Branch


@dataclasses.dataclass
class BranchRepository(Protocol):
    """Interface for branch repository."""

    def save(self, branch: Branch) -> None:
        """Save a branch."""
        ...

    def has_id(self, branch_id: uuid.UUID) -> bool:
        """Check if the branch exists."""
        ...

    def get_by_id(self, branch_id: uuid.UUID) -> Branch:
        """Retrieve a branch from the repository."""
        ...
