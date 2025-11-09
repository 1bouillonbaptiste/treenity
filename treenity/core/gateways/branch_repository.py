"""Interface for branch repository."""

import dataclasses

from treenity.core.models.branch import Branch


@dataclasses.dataclass
class BranchRepository:
    """Interface for branch repository."""

    def save(self, branch: Branch) -> None:
        """Save a branch."""
        ...
