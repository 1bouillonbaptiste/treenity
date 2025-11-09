"""Interface for branch splitting strategies."""

from typing import Protocol

from treenity.core.models.branch import Branch


class SplitStrategy(Protocol):
    """Interface for branch splitting strategies."""

    def split(self, branch: Branch) -> list[Branch]:
        """Create new children branches from a parent."""
        ...
