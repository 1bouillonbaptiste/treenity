"""Data models for streamlit components."""

import dataclasses


@dataclasses.dataclass
class TreeID:
    """Represents a tree identifier."""

    value: str


@dataclasses.dataclass
class TreeData:
    """Represents tree data for visualization."""

    id: str
    length: int
    children: list["TreeData"]

    def __post_init__(self):
        """Convert children dicts to TreeData objects if needed."""
        if self.children and isinstance(self.children[0], dict):
            self.children = [TreeData(**child) for child in self.children]
