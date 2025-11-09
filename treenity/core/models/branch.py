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

    def grow(self) -> None:
        """Grow the branch."""
        self.length += 1
