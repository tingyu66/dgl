"""Sampled subgraph for CSCSamplingGraph."""
# pylint: disable= invalid-name
from dataclasses import dataclass
from typing import Dict, Tuple, Union

import torch

from ..base import etype_str_to_tuple
from ..sampled_subgraph import SampledSubgraph


@dataclass
class SampledSubgraphImpl(SampledSubgraph):
    r"""Class for sampled subgraph specific for CSCSamplingGraph.

    Examples
    --------
    >>> node_pairs = {"A:relation:B"): (torch.tensor([0, 1, 2]),
    ... torch.tensor([0, 1, 2]))}
    >>> reverse_column_node_ids = {'B': torch.tensor([10, 11, 12])}
    >>> reverse_row_node_ids = {'A': torch.tensor([13, 14, 15])}
    >>> reverse_edge_ids = {"A:relation:B": torch.tensor([19, 20, 21])}
    >>> subgraph = gb.SampledSubgraphImpl(
    ... node_pairs=node_pairs,
    ... reverse_column_node_ids=reverse_column_node_ids,
    ... reverse_row_node_ids=reverse_row_node_ids,
    ... reverse_edge_ids=reverse_edge_ids
    ... )
    >>> print(subgraph.node_pairs)
    {"A:relation:B": (tensor([0, 1, 2]), tensor([0, 1, 2]))}
    >>> print(subgraph.reverse_column_node_ids)
    {'B': tensor([10, 11, 12])}
    >>> print(subgraph.reverse_row_node_ids)
    {'A': tensor([13, 14, 15])}
    >>> print(subgraph.reverse_edge_ids)
    {"A:relation:B": tensor([19, 20, 21])}
    """
    node_pairs: Union[
        Dict[str, Tuple[torch.Tensor, torch.Tensor]],
        Tuple[torch.Tensor, torch.Tensor],
    ] = None
    reverse_column_node_ids: Union[Dict[str, torch.Tensor], torch.Tensor] = None
    reverse_row_node_ids: Union[Dict[str, torch.Tensor], torch.Tensor] = None
    reverse_edge_ids: Union[Dict[str, torch.Tensor], torch.Tensor] = None

    def __post_init__(self):
        if isinstance(self.node_pairs, dict):
            for etype, pair in self.node_pairs.items():
                assert (
                    isinstance(etype, str)
                    and len(etype_str_to_tuple(etype)) == 3
                ), "Edge type should be a string in format of str:str:str."
                assert (
                    isinstance(pair, tuple) and len(pair) == 2
                ), "Node pair should be a source-destination tuple (u, v)."
                assert all(
                    isinstance(item, torch.Tensor) for item in pair
                ), "Nodes in pairs should be of type torch.Tensor."
        else:
            assert (
                isinstance(self.node_pairs, tuple) and len(self.node_pairs) == 2
            ), "Node pair should be a source-destination tuple (u, v)."
            assert all(
                isinstance(item, torch.Tensor) for item in self.node_pairs
            ), "Nodes in pairs should be of type torch.Tensor."
