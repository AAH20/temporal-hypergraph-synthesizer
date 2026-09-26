"""
Data Models for Temporal Hypergraph Synthesizer:
Defines hypernodes, temporal hyperedges, query templates, and isomorphic match results.
Zero external dependencies (pure Python standard library).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple, Set


class SynthesisMode(str, Enum):
    TACTICAL_C2_DETECTION = "TACTICAL_C2_DETECTION"
    INDUSTRIAL_SUPPLY_CHAIN = "INDUSTRIAL_SUPPLY_CHAIN"


@dataclass
class HyperNode:
    """Represents an entity (radio emitter, insurgent courier, or semiconductor broker)."""
    node_id: str
    node_type: str
    attributes: Dict[str, str] = field(default_factory=dict)


@dataclass
class TemporalHyperEdge:
    """Represents a multi-way interaction event occurring at a specific point in time."""
    edge_id: str
    relation_type: str
    participants: List[str]
    timestamp_s: float
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class QueryTemplate:
    """Represents a suspicious C2 cell structure or counterfeit laundering pattern to find."""
    template_id: str
    node_types: Dict[str, str]              # query_node_var -> required node_type
    edge_patterns: List[Tuple[str, List[str]]]  # [(relation_type, [query_node_vars])]
    max_duration_window_s: float            # Maximum timespan for the pattern sequence


@dataclass
class MatchResult:
    """Outcome of temporal dynamic subgraph isomorphism search."""
    mode: SynthesisMode
    matches_found: List[Dict[str, str]]     # List of {query_var: matched_node_id}
    matched_patterns_count: int
    search_latency_ms: float
    total_graph_nodes: int
    total_graph_edges: int
    metrics: Dict[str, float] = field(default_factory=dict)
