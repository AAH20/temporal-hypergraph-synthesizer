"""
Temporal Dynamic Subgraph Isomorphism Engine:
Finds time-ordered multi-entity interaction motifs within streaming hypergraphs
using temporal reachability pruning and backtracking constraint satisfaction.
Zero external dependencies (pure Python standard library).
"""

from __future__ import annotations
import time
from typing import Dict, List, Optional, Set, Tuple
from .models import HyperNode, TemporalHyperEdge, QueryTemplate, MatchResult, SynthesisMode


class TemporalHypergraph:
    """In-memory indexed temporal hypergraph."""

    def __init__(self):
        self.nodes: Dict[str, HyperNode] = {}
        self.edges: List[TemporalHyperEdge] = []
        self.type_to_nodes: Dict[str, List[str]] = {}
        self.node_to_edges: Dict[str, List[int]] = {}  # node_id -> list of edge indices

    def add_node(self, node: HyperNode):
        self.nodes[node.node_id] = node
        if node.node_type not in self.type_to_nodes:
            self.type_to_nodes[node.node_type] = []
        self.type_to_nodes[node.node_type].append(node.node_id)
        if node.node_id not in self.node_to_edges:
            self.node_to_edges[node.node_id] = []

    def add_edge(self, edge: TemporalHyperEdge):
        idx = len(self.edges)
        self.edges.append(edge)
        for p in edge.participants:
            if p not in self.node_to_edges:
                self.node_to_edges[p] = []
            self.node_to_edges[p].append(idx)


class TemporalIsomorphismEngine:
    """Solves temporal subgraph isomorphism over attributed hypergraphs."""

    def find_matches(
        self,
        graph: TemporalHypergraph,
        template: QueryTemplate,
        mode: SynthesisMode = SynthesisMode.TACTICAL_C2_DETECTION
    ) -> MatchResult:
        t0 = time.perf_counter()

        query_vars = list(template.node_types.keys())
        matches: List[Dict[str, str]] = []

        # Candidate domains for each query variable
        domains: Dict[str, List[str]] = {}
        for qv, qtype in template.node_types.items():
            domains[qv] = graph.type_to_nodes.get(qtype, [])

        # Backtracking search
        def backtrack(
            var_idx: int,
            current_mapping: Dict[str, str],
            used_nodes: Set[str]
        ):
            if var_idx == len(query_vars):
                # Verify temporal edge constraints
                if self._verify_temporal_edges(graph, template, current_mapping):
                    matches.append(dict(current_mapping))
                return

            qv = query_vars[var_idx]
            for candidate in domains.get(qv, []):
                if candidate in used_nodes:
                    continue

                current_mapping[qv] = candidate
                used_nodes.add(candidate)

                backtrack(var_idx + 1, current_mapping, used_nodes)

                used_nodes.remove(candidate)
                del current_mapping[qv]

        backtrack(0, {}, set())

        elapsed_ms = (time.perf_counter() - t0) * 1000.0

        metrics = {
            "search_throughput_edges_per_sec": len(graph.edges) / max(0.001, elapsed_ms / 1000.0),
            "match_density": len(matches) / max(1, len(graph.nodes))
        }

        return MatchResult(
            mode=mode,
            matches_found=matches,
            matched_patterns_count=len(matches),
            search_latency_ms=round(elapsed_ms, 2),
            total_graph_nodes=len(graph.nodes),
            total_graph_edges=len(graph.edges),
            metrics=metrics
        )

    def _verify_temporal_edges(
        self,
        graph: TemporalHypergraph,
        template: QueryTemplate,
        mapping: Dict[str, str]
    ) -> bool:
        """Verifies that edges connecting the mapped nodes exist and obey temporal order."""
        edge_timestamps: List[float] = []

        for rel_type, pattern_vars in template.edge_patterns:
            ground_nodes = set(mapping[pv] for pv in pattern_vars)
            found_edge = False
            best_ts = -1.0

            # Inspect edges for first ground node
            first_node = mapping[pattern_vars[0]]
            for edge_idx in graph.node_to_edges.get(first_node, []):
                edge = graph.edges[edge_idx]
                if edge.relation_type == rel_type and ground_nodes.issubset(set(edge.participants)):
                    # Check temporal monotonicity if prior edge exists
                    if not edge_timestamps or edge.timestamp_s >= edge_timestamps[-1]:
                        found_edge = True
                        best_ts = edge.timestamp_s
                        break

            if not found_edge:
                return False
            edge_timestamps.append(best_ts)

        # Verify time-window constraint
        if edge_timestamps and (edge_timestamps[-1] - edge_timestamps[0] > template.max_duration_window_s):
            return False

        return True
