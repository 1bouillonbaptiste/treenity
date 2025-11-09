from treenity.core.grow_tree import GrowTreeUseCase
from treenity.core.models.branch import Branch


def test_should_create_a_branch():
    use_case = GrowTreeUseCase()
    result = use_case.execute()

    assert result == Branch(length=1)
