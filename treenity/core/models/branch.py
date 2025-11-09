"""Define a tree branch."""

import dataclasses


@dataclasses.dataclass
class Branch:
    """Represent a tree branch."""

    length: int = 1

    def grow(self) -> None:
        """Grow the branch."""
        self.length += 1
