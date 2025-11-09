"""Grow a tree from scratch."""

import uuid

from treenity.core.gateways.branch_repository import BranchRepository
from treenity.core.gateways.split_strategy import SplitStrategy
from treenity.core.models.branch import Branch


class GrowTreeUseCase:
    """Grow a tree from scratch."""

    def __init__(self, branch_repository: BranchRepository, split_strategy: SplitStrategy):
        self._branch_repository = branch_repository
        self._split_strategy = split_strategy

    def execute(self, tree_id: uuid.UUID, iterations: int = 1):
        """Execute the use case."""
        if self._branch_repository.has_id(tree_id):
            tree_root = self._branch_repository.get_by_id(tree_id)
        else:
            tree_root = Branch(id=tree_id, length=1)
        for _ in range(iterations):
            self._grow_step(tree_root)

    def _grow_step(self, branch: Branch):
        """Grow a branch by one step."""
        if branch.can_split():
            children_branches = self._split_strategy.split(branch)
            branch.with_children([child.id for child in children_branches])
            for child_branch in children_branches:
                self._branch_repository.save(child_branch)
        else:
            branch.grow()
        self._branch_repository.save(branch)
