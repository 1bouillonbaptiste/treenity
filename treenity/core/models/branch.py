"""Define a tree branch."""

import dataclasses


@dataclasses.dataclass
class Branch:
    """Represent a tree branch."""

    length: int = 1
