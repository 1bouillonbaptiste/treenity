from uuid import UUID

from treenity.adapters.secondary.gateways.in_memory_branch_repository import InMemoryBranchRepository
from treenity.core.grow_tree import GrowTreeUseCase
from treenity.core.models.branch import Branch


def test_should_grow_a_branch():
    fake_branch_repository = InMemoryBranchRepository()
    grow_tree_use_case = GrowTreeUseCase(branch_repository=fake_branch_repository)
    grow_tree_use_case.execute(tree_id=UUID("1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3"), iterations=2)

    assert fake_branch_repository.branches == [Branch(id=UUID("1e39c03a-f7ed-4c5f-b8cb-af75229fd2c3"), length=3)]
