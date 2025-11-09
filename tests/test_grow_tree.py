from uuid import UUID

from treenity.adapters.secondary.gateways.in_memory_branch_repository import InMemoryBranchRepository
from treenity.core.grow_tree import GrowTreeUseCase
from treenity.core.models.branch import Branch


def test_should_grow_a_new_tree_by_two_iterations():
    fake_branch_repository = InMemoryBranchRepository()
    grow_tree_use_case = GrowTreeUseCase(branch_repository=fake_branch_repository)
    grow_tree_use_case.execute(tree_id=UUID("1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3"), iterations=2)

    assert fake_branch_repository.branches == {
        UUID("1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3"): Branch(id=UUID("1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3"), length=3)
    }


def test_should_grow_an_existing_tree_by_three_iterations():
    fake_branch_repository = InMemoryBranchRepository()
    fake_branch_repository.save(Branch(id=UUID("1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3"), length=2))

    grow_tree_use_case = GrowTreeUseCase(branch_repository=fake_branch_repository)
    grow_tree_use_case.execute(tree_id=UUID("1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3"), iterations=3)

    assert fake_branch_repository.branches == {
        UUID("1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3"): Branch(id=UUID("1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3"), length=5)
    }
