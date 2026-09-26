"""
Tactical Insurgent C2 Network Adapter:
Generates temporal intelligence hypergraphs simulating covert commander-courier-scout
communications, dead-drops, and weapon cache rendezvous events.
Zero external dependencies (pure Python standard library).
"""

from __future__ import annotations
import random
from typing import Tuple
from ..core.models import HyperNode, TemporalHyperEdge, QueryTemplate
from ..core.isomorphism_engine import TemporalHypergraph


class InsurgentC2Adapter:
    """Simulates tactical multi-INT signals and human intelligence graphs."""

    @staticmethod
    def create_tactical_c2_scenario(
        noise_nodes: int = 40,
        seed: int = 42
    ) -> Tuple[TemporalHypergraph, QueryTemplate]:
        rng = random.Random(seed)
        graph = TemporalHypergraph()

        # 1. Ground Truth C2 Cell Entities
        graph.add_node(HyperNode("COMMANDER-01", "COMMANDER", {"faction": "RED-CELL"}))
        graph.add_node(HyperNode("COURIER-07", "COURIER", {"alias": "AL-ZUBAYR"}))
        graph.add_node(HyperNode("SCOUT-12", "SCOUT", {"role": "OBSERVER"}))

        # 2. Add Background Noise Entities (Civilians, Merchants, Neutral Radios)
        for i in range(noise_nodes):
            graph.add_node(HyperNode(f"CIVILIAN-{i+1:03d}", "CIVILIAN", {"location": "BAZAAR"}))
            if i % 5 == 0:
                graph.add_node(HyperNode(f"DECOY-COURIER-{i+1:02d}", "COURIER", {"status": "BENIGN"}))

        # 3. Temporal C2 Interaction Chain
        t0 = 1700000000.0  # Epoch base
        # Step A: Commander orders Courier (Radio burst)
        graph.add_edge(TemporalHyperEdge(
            edge_id="EVENT-01",
            relation_type="DISPATCH_ORDER",
            participants=["COMMANDER-01", "COURIER-07"],
            timestamp_s=t0 + 120.0
        ))

        # Step B: Courier meets Scout at dead-drop location
        graph.add_edge(TemporalHyperEdge(
            edge_id="EVENT-02",
            relation_type="DEAD_DROP_HANDOFF",
            participants=["COURIER-07", "SCOUT-12"],
            timestamp_s=t0 + 450.0
        ))

        # 4. Add Background Traffic Edges
        for j in range(noise_nodes * 2):
            p1 = f"CIVILIAN-{rng.randint(1, noise_nodes):03d}"
            p2 = f"CIVILIAN-{rng.randint(1, noise_nodes):03d}"
            graph.add_edge(TemporalHyperEdge(
                edge_id=f"NOISE-EVENT-{j+1:03d}",
                relation_type="PHONE_CALL",
                participants=[p1, p2],
                timestamp_s=t0 + rng.uniform(0.0, 1000.0)
            ))

        # 5. Suspicious Motif Query Template
        template = QueryTemplate(
            template_id="INSURGENT-C2-DISPATCH-DEAD-DROP",
            node_types={
                "?commander": "COMMANDER",
                "?courier": "COURIER",
                "?scout": "SCOUT"
            },
            edge_patterns=[
                ("DISPATCH_ORDER", ["?commander", "?courier"]),
                ("DEAD_DROP_HANDOFF", ["?courier", "?scout"])
            ],
            max_duration_window_s=600.0  # Must occur within 10 minutes
        )

        return graph, template
