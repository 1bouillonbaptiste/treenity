"""Grow a tree from scratch."""

import uuid

from treenity.core.gateways.branch_repository import BranchRepository
from treenity.core.models.branch import Branch


class GrowTreeUseCase:
    """Grow a tree from scratch."""

    def __init__(self, branch_repository: BranchRepository):
        self._branch_repository = branch_repository

    def execute(self, tree_id: uuid.UUID, iterations: int = 1):
        """Execute the use case."""
        if self._branch_repository.has_id(tree_id):
            tree_root = self._branch_repository.get_by_id(tree_id)
        else:
            tree_root = Branch(id=tree_id, length=1)
        for _ in range(iterations):
            tree_root.grow()
        self._branch_repository.save(tree_root)
