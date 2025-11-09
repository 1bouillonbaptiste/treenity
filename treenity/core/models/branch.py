"""Define a tree branch."""

import dataclasses
import uuid


@dataclasses.dataclass
class Branch:
    """Represent a tree branch."""

    id: uuid.UUID
    """Branch unique identifier."""

    length: int = 1
    """Length of the branch."""

    children_ids: list[uuid.UUID] = dataclasses.field(default_factory=list)
    """Children branches of this branch."""

    def grow(self) -> None:
        """Grow the branch."""
        self.length += 1

    def can_split(self) -> bool:
        """Check if the branch can be split."""
        return self.length >= 5

    def with_children(self, children_ids: list[uuid.UUID]) -> None:
        """Set the children of this branch."""
        self.children_ids = children_ids
