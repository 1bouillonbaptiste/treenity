from treenity.adapters.primary.streamlit.components.tree_visualizer import (
    TreeData,
    TreeVisualizer,
)


def test_can_display_a_tree_with_branches():
    tree_visualizer = TreeVisualizer()

    tree_data = TreeData(
        id="dacdc524-d1a5-485c-aef9-7a616d83d1ba",
        length=7,
        children=[
            TreeData(id="bffd9ffe-8d78-496b-92de-e05e07250eb0", length=3, children=[]),
            TreeData(id="8b5f3c51-476e-4ced-a876-303be187893e", length=3, children=[]),
        ],
    )

    fig = tree_visualizer.create_tree_plot(tree_data=tree_data)

    assert fig is not None
