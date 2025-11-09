from treenity.core.grow_tree import GrowTreeUseCase
from treenity.core.models.branch import Branch


def test_should_grow_a_branch():
    use_case = GrowTreeUseCase()
    result = use_case.execute(iterations=1)

    assert result == Branch(length=2)
