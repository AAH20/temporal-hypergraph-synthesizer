"""
Temporal Hypergraph Synthesizer Master Facade:
Unifies temporal dynamic subgraph isomorphism across tactical insurgent C2 cell detection
and aerospace semiconductor supply chain counterfeit tracking.
Zero external dependencies (pure Python standard library).
"""

from __future__ import annotations
from typing import Dict, List, Tuple
from .core.models import HyperNode, TemporalHyperEdge, QueryTemplate, MatchResult, SynthesisMode
from .core.isomorphism_engine import TemporalHypergraph, TemporalIsomorphismEngine
from .adapters.defense import InsurgentC2Adapter
from .adapters.industrial import SupplyChainTraceAdapter


class TemporalHypergraphSynthesizer:
    """Master facade for streaming temporal hypergraph motif detection."""

    def __init__(self):
        self.engine = TemporalIsomorphismEngine()

    def detect_tactical_c2_cells(self, noise_nodes: int = 40, seed: int = 42) -> MatchResult:
        """Finds suspicious insurgent C2 communications motifs."""
        graph, template = InsurgentC2Adapter.create_tactical_c2_scenario(noise_nodes=noise_nodes, seed=seed)
        return self.engine.find_matches(graph, template, mode=SynthesisMode.TACTICAL_C2_DETECTION)

    def trace_counterfeit_supply_chains(self, benign_suppliers: int = 30, seed: int = 42) -> MatchResult:
        """Finds fraudulent semiconductor laundering supply-chain chains."""
        graph, template = SupplyChainTraceAdapter.create_counterfeit_laundering_scenario(benign_suppliers=benign_suppliers, seed=seed)
        return self.engine.find_matches(graph, template, mode=SynthesisMode.INDUSTRIAL_SUPPLY_CHAIN)

    def query_custom_graph(
        self,
        graph: TemporalHypergraph,
        template: QueryTemplate,
        mode: SynthesisMode = SynthesisMode.TACTICAL_C2_DETECTION
    ) -> MatchResult:
        """Executes custom temporal query over provided hypergraph."""
        return self.engine.find_matches(graph, template, mode=mode)
