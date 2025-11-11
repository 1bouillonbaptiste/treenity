"""Tree visualization component using Plotly."""

import dataclasses
import math
from typing import NamedTuple

import plotly.graph_objects as go
from plotly.graph_objects import Figure

from treenity.adapters.primary.streamlit.components.models import TreeData

Position = NamedTuple("Position", [("x", float), ("y", float)])


@dataclasses.dataclass
class TreeLeaf:
    """Store leaf data."""

    position: Position


@dataclasses.dataclass
class TreeBranch:
    """Store branch data."""

    from_position: Position
    to_position: Position

    @property
    def size(self):
        """Calculate branch size."""
        length_x = self.to_position.x - self.from_position.x
        length_y = self.to_position.y - self.from_position.y
        return (length_x**2 + length_y**2) ** 0.5

    @property
    def length(self):
        """Calculate branch length."""
        return self.size**0.5

    @property
    def diameter(self):
        """Calculate branch diameter."""
        return math.log2(1 + self.size)


@dataclasses.dataclass
class Tree:
    """Represent a tree."""

    branches: list[TreeBranch]
    leaves: list[TreeLeaf]


@dataclasses.dataclass
class TreeStats:
    """Store tree statistics."""

    total_branches: int
    max_depth: int
    leaf_count: int


class TreeVisualizer:
    """Handles tree visualization using Plotly."""

    def create_tree_plot(self, tree_data: TreeData) -> Figure:
        """Create an interactive tree plot using Plotly."""
        tree = _extract_tree_structure(tree_data)

        fig = go.Figure()

        # Display branches
        for branch in tree.branches:
            fig.add_trace(
                go.Scatter(
                    x=[branch.from_position.x, branch.to_position.x],
                    y=[branch.from_position.y, branch.to_position.y],
                    mode="lines",
                    line=dict(color="#7f8c8d", width=branch.diameter),  # noqa: C408
                    hoverinfo="none",
                    showlegend=False,
                )
            )

        # Display leaves
        leaves_x = [leaf.position.x for leaf in tree.leaves]
        leaves_y = [leaf.position.y for leaf in tree.leaves]

        fig.add_trace(
            go.Scatter(
                x=leaves_x,
                y=leaves_y,
                mode="markers",
                marker=dict(size=20, color="green", line=dict(width=2, color="darkgreen")),  # noqa: C408
                hoverinfo="text",
                name="Leaves",
            )
        )

        # Update layout
        fig.update_layout(
            title={"text": "🌳 Tree Structure", "x": 0.5, "xanchor": "center"},
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),  # noqa: C408
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),  # noqa: C408
            plot_bgcolor="white",
            height=600,
            margin=dict(l=20, r=20, t=60, b=20),  # noqa: C408
        )

        return fig

    def calculate_tree_stats(self, tree_data: TreeData) -> TreeStats:
        """Calculate tree statistics."""
        stats = TreeStats(total_branches=0, max_depth=0, leaf_count=0)

        def _count_nodes(branch: TreeData, depth=0):
            """Recursively count nodes and calculate stats."""
            stats.total_branches += 1
            stats.max_depth = max(stats.max_depth, depth)

            children = branch.children
            if not children:
                stats.leaf_count += 1
            else:
                for child in children:
                    _count_nodes(child, depth + 1)

        _count_nodes(tree_data)
        return stats


def _extract_tree_structure(tree_data: TreeData) -> Tree:
    """Extract nodes and edges from tree data for visualization."""
    branches = []
    leaves = []

    def _traverse(branch: TreeData, current_position: Position, parent_angle: float):
        """Recursively traverse tree and calculate positions using angles."""
        if not branch.children:
            leaves.append(TreeLeaf(position=current_position))
        else:
            child_count = len(branch.children)

            start_angle = parent_angle
            angle_step: float = 0
            if child_count > 1:
                # Multiple children: spread between -45° and +45° from the parent direction
                spread_range = 90
                start_angle = max([0, parent_angle - spread_range / 2])
                end_angle = min([180, parent_angle + spread_range / 2])
                angle_step = (end_angle - start_angle) / (child_count - 1) if child_count > 1 else 0

            for i, child in enumerate(branch.children):
                child_angle = start_angle + (angle_step * i)

                # Convert angle to radians and calculate position
                angle_rad = math.radians(child_angle)
                branch_length = child.length

                child_position = Position(
                    x=current_position.x + branch_length * math.cos(angle_rad),
                    y=current_position.y + branch_length * math.sin(angle_rad),
                )
                branches.append(TreeBranch(from_position=current_position, to_position=child_position))

                _traverse(branch=child, current_position=child_position, parent_angle=child_angle)

    first_branch = TreeBranch(from_position=Position(x=0, y=0), to_position=Position(x=0, y=tree_data.length))
    branches.append(first_branch)

    _traverse(branch=tree_data, current_position=first_branch.to_position, parent_angle=90)
    return Tree(branches=branches, leaves=leaves)
