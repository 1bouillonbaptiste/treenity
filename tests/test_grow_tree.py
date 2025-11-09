import dataclasses
from uuid import UUID

import pytest

from treenity.adapters.secondary.gateways.in_memory_branch_repository import InMemoryBranchRepository
from treenity.core.gateways.split_strategy import SplitStrategy
from treenity.core.grow_tree import GrowTreeUseCase
from treenity.core.models.branch import Branch


@dataclasses.dataclass
class FakeSplitStrategy(SplitStrategy):
    def __init__(self):
        self._active = False

    def activate(self):
        self._active = True

    def split(self, branch: Branch) -> list[Branch]:
        """Create two new branches."""
        if self._active:
            return [
                Branch(id=UUID("dcf8b64a-dac7-4644-b89f-040b2d07457f"), length=1),
                Branch(id=UUID("33e8ec10-acc5-49ec-a716-958ddb9bf9c5"), length=1),
            ]
        return []


@dataclasses.dataclass
class TestingContext:
    """Context for this test."""

    branch_repository: InMemoryBranchRepository
    split_strategy: FakeSplitStrategy
    grow_tree_use_case: GrowTreeUseCase


@pytest.fixture
def this_context():
    fake_branch_repository = InMemoryBranchRepository()
    fake_split_strategy = FakeSplitStrategy()
    return TestingContext(
        branch_repository=fake_branch_repository,
        split_strategy=fake_split_strategy,
        grow_tree_use_case=GrowTreeUseCase(
            branch_repository=fake_branch_repository, split_strategy=fake_split_strategy
        ),
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


def test_should_not_split_on_small_branch(this_context: TestingContext):
    # Given
    this_context.branch_repository.save(Branch(id=UUID("1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3"), length=2))
    this_context.split_strategy.activate()

    # When
    this_context.grow_tree_use_case.execute(tree_id=UUID("1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3"), iterations=1)

    # Then
    assert this_context.branch_repository.branches == {
        UUID("1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3"): Branch(
            id=UUID("1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3"),
            length=3,
        ),
    }


def test_should_create_two_new_branches_on_split(this_context: TestingContext):
    # Given
    this_context.branch_repository.save(Branch(id=UUID("1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3"), length=6))
    this_context.split_strategy.activate()

    # When
    this_context.grow_tree_use_case.execute(tree_id=UUID("1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3"), iterations=1)

    # Then
    assert this_context.branch_repository.branches == {
        UUID("1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3"): Branch(
            id=UUID("1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3"),
            length=6,
            children_ids=[UUID("dcf8b64a-dac7-4644-b89f-040b2d07457f"), UUID("33e8ec10-acc5-49ec-a716-958ddb9bf9c5")],
        ),
        UUID("dcf8b64a-dac7-4644-b89f-040b2d07457f"): Branch(id=UUID("dcf8b64a-dac7-4644-b89f-040b2d07457f"), length=1),
        UUID("33e8ec10-acc5-49ec-a716-958ddb9bf9c5"): Branch(id=UUID("33e8ec10-acc5-49ec-a716-958ddb9bf9c5"), length=1),
    }


def test_should_not_split_on_existing_children(this_context: TestingContext):
    # Given
    this_context.branch_repository.save(
        Branch(
            id=UUID("1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3"),
            length=6,
            children_ids=[UUID("dcf8b64a-dac7-4644-b89f-040b2d07457f"), UUID("33e8ec10-acc5-49ec-a716-958ddb9bf9c5")],
        )
    )
    this_context.branch_repository.save(Branch(id=UUID("dcf8b64a-dac7-4644-b89f-040b2d07457f"), length=1))
    this_context.branch_repository.save(Branch(id=UUID("33e8ec10-acc5-49ec-a716-958ddb9bf9c5"), length=1))
    this_context.split_strategy.activate()

    # When
    this_context.grow_tree_use_case.execute(tree_id=UUID("1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3"), iterations=1)

    # Then
    assert this_context.branch_repository.branches == {
        UUID("1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3"): Branch(
            id=UUID("1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3"),
            length=7,
            children_ids=[UUID("dcf8b64a-dac7-4644-b89f-040b2d07457f"), UUID("33e8ec10-acc5-49ec-a716-958ddb9bf9c5")],
        ),
        UUID("dcf8b64a-dac7-4644-b89f-040b2d07457f"): Branch(id=UUID("dcf8b64a-dac7-4644-b89f-040b2d07457f"), length=2),
        UUID("33e8ec10-acc5-49ec-a716-958ddb9bf9c5"): Branch(id=UUID("33e8ec10-acc5-49ec-a716-958ddb9bf9c5"), length=2),
    }


def test_should_split_a_child_branch(this_context: TestingContext):
    # Given
    this_context.branch_repository.save(
        Branch(
            id=UUID("1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3"),
            length=6,
            children_ids=[UUID("0b6dce72-31d7-41e1-aed4-6d58983621a1")],
        )
    )
    this_context.branch_repository.save(
        Branch(
            id=UUID("0b6dce72-31d7-41e1-aed4-6d58983621a1"),
            length=6,
        )
    )
    this_context.split_strategy.activate()

    # When
    this_context.grow_tree_use_case.execute(tree_id=UUID("1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3"), iterations=1)

    # Then
    assert this_context.branch_repository.branches == {
        UUID("1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3"): Branch(
            id=UUID("1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3"),
            length=7,
            children_ids=[UUID("0b6dce72-31d7-41e1-aed4-6d58983621a1")],
        ),
        UUID("0b6dce72-31d7-41e1-aed4-6d58983621a1"): Branch(
            id=UUID("0b6dce72-31d7-41e1-aed4-6d58983621a1"),
            length=6,
            children_ids=[UUID("dcf8b64a-dac7-4644-b89f-040b2d07457f"), UUID("33e8ec10-acc5-49ec-a716-958ddb9bf9c5")],
        ),
        UUID("dcf8b64a-dac7-4644-b89f-040b2d07457f"): Branch(id=UUID("dcf8b64a-dac7-4644-b89f-040b2d07457f"), length=1),
        UUID("33e8ec10-acc5-49ec-a716-958ddb9bf9c5"): Branch(id=UUID("33e8ec10-acc5-49ec-a716-958ddb9bf9c5"), length=1),
    }
