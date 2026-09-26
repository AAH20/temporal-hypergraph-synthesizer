"""
Temporal Hypergraph Synthesizer:
Dual-Use Temporal Dynamic Subgraph Isomorphism Engine for Tactical C2 & Counterfeit Tracing.
Zero external dependencies (pure Python standard library).
"""

from .core.models import (
    HyperNode,
    TemporalHyperEdge,
    QueryTemplate,
    MatchResult,
    SynthesisMode
)
from .core.isomorphism_engine import TemporalHypergraph, TemporalIsomorphismEngine
from .adapters.defense import InsurgentC2Adapter
from .adapters.industrial import SupplyChainTraceAdapter
from .synthesizer import TemporalHypergraphSynthesizer

__all__ = [
    "HyperNode",
    "TemporalHyperEdge",
    "QueryTemplate",
    "MatchResult",
    "SynthesisMode",
    "TemporalHypergraph",
    "TemporalIsomorphismEngine",
    "InsurgentC2Adapter",
    "SupplyChainTraceAdapter",
    "TemporalHypergraphSynthesizer"
]

__version__ = "1.0.0"
