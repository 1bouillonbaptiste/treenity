from uuid import UUID

from hypothesis import given
from hypothesis import strategies as some

from treenity.adapters.secondary.gateways.in_memory_branch_repository import InMemoryBranchRepository
from treenity.adapters.secondary.gateways.random_split_strategy import RandomSplitStrategy
from treenity.core.gateways.branch_repository import BranchRepository
from treenity.core.grow_tree import GrowTreeUseCase
from treenity.core.models.branch import Branch


def _assert_children_shorter_than_parent(branch: Branch, branch_repository: BranchRepository):
    for child in branch.children_ids:
        child_branch = branch_repository.get_by_id(child)
        assert child_branch.length <= branch.length
        _assert_children_shorter_than_parent(child_branch, branch_repository)


@given(some.integers(min_value=1, max_value=100))
def test_children_shorter_than_parents_property(num_iterations: int):
    # Given
    fake_branch_repository = InMemoryBranchRepository()
    fake_split_strategy = RandomSplitStrategy(split_probability=0.1)
    grow_tree_use_case = GrowTreeUseCase(branch_repository=fake_branch_repository, split_strategy=fake_split_strategy)

    # When
    grow_tree_use_case.execute(tree_id=UUID("1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3"), iterations=num_iterations)

    tree_root = fake_branch_repository.get_by_id(branch_id=UUID("1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3"))
    _assert_children_shorter_than_parent(tree_root, branch_repository=fake_branch_repository)
