"""Main Streamlit dashboard for tree visualization."""

import streamlit

from treenity.adapters.primary.streamlit.components.api_client import TreeAPIClient
from treenity.adapters.primary.streamlit.components.tree_visualizer import TreeVisualizer

# Configure page
streamlit.set_page_config(
    page_title="🌳 Treenity Dashboard", page_icon="🌳", layout="wide", initial_sidebar_state="collapsed"
)

# Initialize components
api_client = TreeAPIClient()
visualizer = TreeVisualizer()


def main():
    """Main dashboard application."""
    # Title and description
    streamlit.title("🌳 Treenity Dashboard")
    streamlit.markdown("Generate and visualize trees using the GrowTreeUseCase")

    # Create two columns for better layout
    col1, col2 = streamlit.columns([1, 3])

    with col1:
        streamlit.subheader("⚙️ Controls")

        # Input controls
        iterations = streamlit.number_input(
            "Number of iterations", min_value=1, max_value=100, value=5, help="How many growth iterations to perform"
        )

        # Generate button
        generate_clicked = streamlit.button("🌱 Generate Tree", type="primary", use_container_width=True)

        # Status section
        streamlit.subheader("📊 Status")

        # Initialize session state
        if "tree_data" not in streamlit.session_state:
            streamlit.session_state.tree_data = None
        if "generation_info" not in streamlit.session_state:
            streamlit.session_state.generation_info = None

    with col2:
        streamlit.subheader("🌳 Tree Visualization")

        # Handle generate button click
        if generate_clicked:
            with streamlit.spinner("Generating tree..."):
                try:
                    # Generate tree via API
                    tree_id = api_client.generate_tree(iterations)
                    streamlit.session_state.generation_info = tree_id

                    # Get tree data
                    tree_data = api_client.get_tree(tree_id=tree_id.value)
                    streamlit.session_state.tree_data = tree_data

                    # Show success message in col1
                    with col1:
                        streamlit.success(f"✅ Successfully generated tree with {iterations} iterations.")
                        streamlit.info(f"🆔 Tree ID: {tree_id.value[:8]}...")

                except Exception as e:
                    with col1:
                        streamlit.error(f"❌ Error: {e!s}")

        # Display tree visualization
        if streamlit.session_state.tree_data:
            try:
                fig = visualizer.create_tree_plot(streamlit.session_state.tree_data)
                streamlit.plotly_chart(fig, use_container_width=True, height=600)

                # Show tree statistics in col1
                with col1:
                    stats = visualizer.calculate_tree_stats(streamlit.session_state.tree_data)
                    streamlit.subheader("📈 Tree Stats")
                    streamlit.metric("Total Branches", stats.total_branches)
                    streamlit.metric("Tree Depth", stats.max_depth)
                    streamlit.metric("Leaf Nodes", stats.leaf_count)

            except Exception as e:
                streamlit.error(f"❌ Visualization error: {e!s}")
        else:
            # Placeholder when no tree is generated
            streamlit.info("👆 Click 'Generate Tree' to create and visualize a tree")
            streamlit.image(
                "https://via.placeholder.com/400x300/f0f2f6/718096?text=Tree+Will+Appear+Here",
                caption="Tree visualization area",
            )


if __name__ == "__main__":
    main()
