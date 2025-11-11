"""Implements `SplitStrategy` with two children branches."""

import random
import uuid

from treenity.core.gateways.split_strategy import SplitStrategy
from treenity.core.models.branch import Branch


class RandomSplitStrategy(SplitStrategy):
    """Dual split strategy."""

    def __init__(self, split_probability):
        self._split_probability = split_probability

    def split(self, branch: Branch) -> list[Branch]:
        """Split a branch into two children branches."""
        if random.random() < self._split_probability:  # noqa: S311, random.random() is not a security risk here
            num_branches = random.randint(1, 3)  # noqa: S311, random.randint() is not a security risk here
            return [Branch(id=uuid.uuid4(), length=1) for _ in range(num_branches)]
        return []
