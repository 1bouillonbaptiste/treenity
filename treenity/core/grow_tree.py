"""Grow a tree from scratch."""

from treenity.core.models.branch import Branch


class GrowTreeUseCase:
    """Grow a tree from scratch."""

    def __init__(self):
        pass

    def execute(self):
        """Execute the use case."""
        return Branch(length=1)
