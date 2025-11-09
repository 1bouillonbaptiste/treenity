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
        has_children = len(self.children_ids) > 0
        is_long_enough = self.length >= 5
        return is_long_enough and not has_children

    def with_children(self, children_ids: list[uuid.UUID]) -> None:
        """Set the children of this branch."""
        self.children_ids = children_ids
