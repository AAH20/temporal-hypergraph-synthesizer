"""
Aerospace Supply Chain Counterfeit Tracing Adapter:
Generates component procurement hypergraphs simulating gray-market broker laundering,
unauthorized lot number re-marking, and defense avionics supply chain injection.
Zero external dependencies (pure Python standard library).
"""

from __future__ import annotations
import random
from typing import Tuple
from ..core.models import HyperNode, TemporalHyperEdge, QueryTemplate
from ..core.isomorphism_engine import TemporalHypergraph


class SupplyChainTraceAdapter:
    """Simulates semiconductor supply chain traceability and counterfeit detection."""

    @staticmethod
    def create_counterfeit_laundering_scenario(
        benign_suppliers: int = 30,
        seed: int = 42
    ) -> Tuple[TemporalHypergraph, QueryTemplate]:
        rng = random.Random(seed)
        graph = TemporalHypergraph()

        # 1. Laundering Syndicate Entities
        graph.add_node(HyperNode("SHADY-BROKER-X", "GRAY_BROKER", {"jurisdiction": "UNREGULATED"}))
        graph.add_node(HyperNode("REMARKING-LAB-7", "REMARKING_FACILITY", {"capability": "LASER_ETCH"}))
        graph.add_node(HyperNode("TIER1-DEFENSE-SUPPLIER", "CERTIFIED_DISTRIBUTOR", {"cage_code": "81205"}))

        # 2. Benign Industry Nodes
        for i in range(benign_suppliers):
            graph.add_node(HyperNode(f"OEM-SUPPLIER-{i+1:02d}", "OEM_FOUNDRY", {"cert": "ISO9001"}))
            graph.add_node(HyperNode(f"LEGIT-DISTRIBUTOR-{i+1:02d}", "CERTIFIED_DISTRIBUTOR", {"cert": "AS9100"}))

        t0 = 1700000000.0
        # Laundering Chain:
        # Step 1: Gray broker ships discarded scrap chips to re-marking facility
        graph.add_edge(TemporalHyperEdge(
            edge_id="SHIP-01",
            relation_type="TRANSFER_UNTESTED_LOT",
            participants=["SHADY-BROKER-X", "REMARKING-LAB-7"],
            timestamp_s=t0 + 1000.0
        ))

        # Step 2: Re-marking facility sells counterfeit mil-spec parts to tier-1 distributor
        graph.add_edge(TemporalHyperEdge(
            edge_id="SHIP-02",
            relation_type="SELL_FRAUDULENT_CERTIFICATE",
            participants=["REMARKING-LAB-7", "TIER1-DEFENSE-SUPPLIER"],
            timestamp_s=t0 + 3500.0
        ))

        # 3. Add legitimate transaction volume
        for j in range(benign_suppliers):
            s1 = f"OEM-SUPPLIER-{j+1:02d}"
            d1 = f"LEGIT-DISTRIBUTOR-{j+1:02d}"
            graph.add_edge(TemporalHyperEdge(
                edge_id=f"LEGIT-SALE-{j+1:02d}",
                relation_type="CERTIFIED_CHIP_SALE",
                participants=[s1, d1],
                timestamp_s=t0 + rng.uniform(0.0, 5000.0)
            ))

        # Query Template: Gray broker -> Remarker -> Certified Distributor
        template = QueryTemplate(
            template_id="COUNTERFEIT-CHIP-LAUNDERING-MOTIF",
            node_types={
                "?broker": "GRAY_BROKER",
                "?remarker": "REMARKING_FACILITY",
                "?buyer": "CERTIFIED_DISTRIBUTOR"
            },
            edge_patterns=[
                ("TRANSFER_UNTESTED_LOT", ["?broker", "?remarker"]),
                ("SELL_FRAUDULENT_CERTIFICATE", ["?remarker", "?buyer"])
            ],
            max_duration_window_s=5000.0
        )

        return graph, template
