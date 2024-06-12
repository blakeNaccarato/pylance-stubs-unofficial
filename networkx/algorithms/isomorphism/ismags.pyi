from typing import Mapping

from ...classes.graph import Graph

__all__ = ["ISMAGS"]

import itertools
from collections import Counter, defaultdict
from functools import reduce, wraps

def are_all_equal(iterable) -> bool: ...
def make_partitions(items, test): ...
def partition_to_color(partitions) -> Mapping: ...
def intersect(collection_of_sets) -> set: ...

class ISMAGS:
    def __init__(
        self,
        graph: Graph,
        subgraph: Graph,
        node_match=None,
        edge_match=None,
        cache=None,
    ): ...
    @property
    def _sgn_partitions(self): ...
    @property
    def _sge_partitions(self): ...
    @property
    def _gn_partitions(self): ...
    @property
    def _ge_partitions(self): ...
    @property
    def _sgn_colors(self): ...
    @property
    def _sge_colors(self): ...
    @property
    def _gn_colors(self): ...
    @property
    def _ge_colors(self): ...
    @property
    def _node_compatibility(self): ...
    @property
    def _edge_compatibility(self): ...
    @staticmethod
    def _node_match_maker(cmp): ...
    @staticmethod
    def _edge_match_maker(cmp): ...
    def find_isomorphisms(self, symmetry: bool = True): ...
    @staticmethod
    def _find_neighbor_color_count(graph, node, node_color, edge_color): ...
    def _get_lookahead_candidates(self): ...
    def largest_common_subgraph(self, symmetry: bool = True): ...
    def analyze_symmetry(self, graph: Graph, node_partitions, edge_colors): ...
    def is_isomorphic(self, symmetry=False) -> bool: ...
    def subgraph_is_isomorphic(self, symmetry=False) -> bool: ...
    def isomorphisms_iter(self, symmetry=True): ...
    def subgraph_isomorphisms_iter(self, symmetry=True): ...
    def _find_nodecolor_candidates(self): ...
    @staticmethod
    def _make_constraints(cosets): ...
    @staticmethod
    def _find_node_edge_color(graph, node_colors, edge_colors): ...
    @staticmethod
    def _get_permutations_by_length(items): ...
    @classmethod
    def _refine_node_partitions(cls, graph, node_partitions, edge_colors, branch=False): ...
    def _edges_of_same_color(self, sgn1, sgn2): ...
    def _map_nodes(self, sgn, candidates, constraints, mapping=None, to_be_mapped=None): ...
    def _largest_common_subgraph(self, candidates, constraints, to_be_mapped=None): ...
    @staticmethod
    def _remove_node(node, nodes, constraints): ...
    @staticmethod
    def _find_permutations(top_partitions, bottom_partitions): ...
    @staticmethod
    def _update_orbits(orbits, permutations): ...
    def _couple_nodes(
        self,
        top_partitions,
        bottom_partitions,
        pair_idx,
        t_node,
        b_node,
        graph,
        edge_colors,
    ): ...
    def _process_ordered_pair_partitions(
        self,
        graph,
        top_partitions,
        bottom_partitions,
        edge_colors,
        orbits=None,
        cosets=None,
    ): ...
