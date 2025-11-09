import dataclasses
from uuid import UUID

import pytest

from treenity.adapters.secondary.gateways.in_memory_branch_repository import InMemoryBranchRepository
from treenity.core.grow_tree import GrowTreeUseCase
from treenity.core.models.branch import Branch


@dataclasses.dataclass
class TestingContext:
    """Context for this test."""

    branch_repository: InMemoryBranchRepository
    grow_tree_use_case: GrowTreeUseCase


@pytest.fixture
def this_context():
    fake_branch_repository = InMemoryBranchRepository()
    return TestingContext(
        branch_repository=fake_branch_repository,
        grow_tree_use_case=GrowTreeUseCase(branch_repository=fake_branch_repository),
    )


def test_should_grow_a_new_tree_by_two_iterations(this_context: TestingContext):
    # When
    this_context.grow_tree_use_case.execute(tree_id=UUID("1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3"), iterations=2)

    # Then
    assert this_context.branch_repository.branches == {
        UUID("1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3"): Branch(id=UUID("1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3"), length=3)
    }


def test_should_grow_an_existing_tree_by_three_iterations(this_context: TestingContext):
    # Given
    this_context.branch_repository.save(Branch(id=UUID("1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3"), length=2))

    # When
    this_context.grow_tree_use_case.execute(tree_id=UUID("1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3"), iterations=3)

    # Then
    assert this_context.branch_repository.branches == {
        UUID("1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3"): Branch(id=UUID("1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3"), length=5)
    }
