"""
DAG related functions.
"""
import collections
import itertools
from typing import Deque, List, Optional, Set, Tuple

from datajunction_server.models import Column
from datajunction_server.models.node import DimensionAttributeOutput, Node, NodeType
from datajunction_server.utils import get_settings

settings = get_settings()


def get_dimensions(node: Node) -> List[DimensionAttributeOutput]:
    """
    Return all available dimensions for a given node.
    """
    dimensions = []

    # Start with the node itself or the node's immediate parent if it's a metric node
    node_starting_state = (node, None)
    immediate_parent_starting_state = [
        (parent, None)
        for parent in (node.current.parents if node.type == NodeType.METRIC else [])
    ]
    to_process: Deque[Tuple[Node, Optional[Column]]] = collections.deque(
        [node_starting_state, *immediate_parent_starting_state],
    )
    processed: Set[Node] = set()
    multi_link_dimensions: Set[str] = set()

    while to_process:
        current_node, link_column = to_process.popleft()

        # Don't include attributes from deactivated dimensions
        if current_node.deactivated_at:
            continue
        processed.add(current_node)

        # Update multi-link dimensions set
        columns_per_dimension = itertools.groupby(
            sorted(
                [col for col in current_node.current.columns if col.dimension],
                key=lambda x: x.dimension.name,
            ),
            key=lambda x: x.dimension.name,
        )
        grouped_dims = {dim: list(values) for dim, values in columns_per_dimension}
        multi_link_dimensions = multi_link_dimensions.union(
            {dim for dim, values in grouped_dims.items() if len(values) > 1},
        )

        for column in current_node.current.columns:
            # Include the dimension if it's a column belonging to a dimension node
            # or if it's tagged with the dimension column attribute
            if (
                current_node.type == NodeType.DIMENSION
                or any(
                    attr.attribute_type.name == "dimension"
                    for attr in column.attributes
                )
                or column.dimension
            ):
                link_col = (
                    link_column.name + "."
                    if link_column is not None
                    and link_column.dimension
                    and link_column.dimension.name in multi_link_dimensions
                    else ""
                )
                dimensions.append(
                    DimensionAttributeOutput(
                        name=f"{link_col}{current_node.name}.{column.name}",
                        type=column.type,
                    ),
                )
            if column.dimension and column.dimension not in processed:
                to_process.append((column.dimension, column))
    return sorted(dimensions, key=lambda x: x.name)


def get_shared_dimensions(
    metric_nodes: List[Node],
) -> List[DimensionAttributeOutput]:
    """
    Return a list of dimensions that are common between the nodes.
    """
    common = {dim.name: dim for dim in get_dimensions(metric_nodes[0])}
    for node in set(metric_nodes[1:]):
        node_dimensions = {dim.name: dim for dim in get_dimensions(node)}
        common_dim_keys = common.keys() & node_dimensions.keys()
        common = {dim: node_dimensions[dim] for dim in common_dim_keys}
    return sorted(common.values(), key=lambda x: x.name)
