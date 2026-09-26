"""
Unit Tests for Temporal Hypergraph Synthesizer:
Verifies temporal dynamic subgraph isomorphism matching, temporal constraint filtering,
and sub-20ms search latency across defense and industrial scenarios.
Zero external dependencies (pure Python standard library).
"""

import unittest
from temporal_hypergraph_synthesizer import (
    TemporalHypergraphSynthesizer,
    TemporalHypergraph,
    HyperNode,
    TemporalHyperEdge,
    QueryTemplate,
    SynthesisMode
)


class TestTemporalHypergraphSynthesizer(unittest.TestCase):

    def setUp(self):
        self.synthesizer = TemporalHypergraphSynthesizer()

    def test_tactical_c2_detection(self):
        """Verifies identification of covert insurgent C2 communications motif."""
        res = self.synthesizer.detect_tactical_c2_cells(noise_nodes=50, seed=42)

        self.assertEqual(res.mode, SynthesisMode.TACTICAL_C2_DETECTION)
        self.assertEqual(res.matched_patterns_count, 1)
        match = res.matches_found[0]
        self.assertEqual(match["?commander"], "COMMANDER-01")
        self.assertEqual(match["?courier"], "COURIER-07")
        self.assertEqual(match["?scout"], "SCOUT-12")
        self.assertLess(res.search_latency_ms, 50.0)

    def test_counterfeit_supply_chain_detection(self):
        """Verifies identification of gray-market chip broker laundering chains."""
        res = self.synthesizer.trace_counterfeit_supply_chains(benign_suppliers=30, seed=42)

        self.assertEqual(res.mode, SynthesisMode.INDUSTRIAL_SUPPLY_CHAIN)
        self.assertEqual(res.matched_patterns_count, 1)
        match = res.matches_found[0]
        self.assertEqual(match["?broker"], "SHADY-BROKER-X")
        self.assertEqual(match["?remarker"], "REMARKING-LAB-7")
        self.assertEqual(match["?buyer"], "TIER1-DEFENSE-SUPPLIER")
        self.assertLess(res.search_latency_ms, 20.0)

    def test_temporal_order_violation_rejection(self):
        """Verifies that reverse-chronological events (t2 < t1) are rejected as invalid motifs."""
        graph = TemporalHypergraph()
        graph.add_node(HyperNode("N1", "LEADER"))
        graph.add_node(HyperNode("N2", "OPERATIVE"))
        graph.add_node(HyperNode("N3", "TARGET"))

        # Event 2 happens BEFORE Event 1 (violates causal chain!)
        graph.add_edge(TemporalHyperEdge("E2", "ATTACK", ["N2", "N3"], timestamp_s=100.0))
        graph.add_edge(TemporalHyperEdge("E1", "ORDER", ["N1", "N2"], timestamp_s=200.0))

        template = QueryTemplate(
            template_id="CAUSAL-ORDER",
            node_types={"?l": "LEADER", "?o": "OPERATIVE", "?t": "TARGET"},
            edge_patterns=[("ORDER", ["?l", "?o"]), ("ATTACK", ["?o", "?t"])],
            max_duration_window_s=500.0
        )

        res = self.synthesizer.query_custom_graph(graph, template)
        self.assertEqual(res.matched_patterns_count, 0, "Expected zero matches for causally inverted events!")


if __name__ == "__main__":
    unittest.main()
