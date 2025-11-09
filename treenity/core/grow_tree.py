"""Grow a tree from scratch."""

from treenity.core.models.branch import Branch


class GrowTreeUseCase:
    """Grow a tree from scratch."""

    def __init__(self):
        pass

    def execute(self, iterations: int = 1):
        """Execute the use case."""
        tree_root = Branch(length=1)
        tree_root.grow()
        return tree_root
