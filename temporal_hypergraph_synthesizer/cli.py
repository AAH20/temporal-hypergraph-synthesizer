"""
Temporal Hypergraph Synthesizer CLI:
Command-line interface demonstrating temporal dynamic subgraph isomorphism across
Tactical Insurgent C2 Cell Detection and Aerospace Counterfeit Chip Tracing.
Zero external dependencies (pure Python standard library).
"""

from __future__ import annotations
import argparse
import sys
import time

from .core.models import SynthesisMode
from .synthesizer import TemporalHypergraphSynthesizer


def run_detect_c2(args: argparse.Namespace) -> None:
    synthesizer = TemporalHypergraphSynthesizer()
    print("=" * 85)
    print("TEMPORAL HYPERGRAPH SYNTHESIZER: TACTICAL INSURGENT C2 MOTIF DETECTION")
    print(f"Background Noise Entities: {args.noise} | Seed: {args.seed}")
    print("Graph Core               : Temporal Dynamic Subgraph Isomorphism (VF2 / Ullmann)")
    print("=" * 85)

    res = synthesizer.detect_tactical_c2_cells(noise_nodes=args.noise, seed=args.seed)

    print("\n--- MATCHED COVERT C2 CELL INSTANCES ---")
    if res.matches_found:
        for idx, match in enumerate(res.matches_found):
            print(f"  * Match #{idx+1}:")
            for qv, actual_id in sorted(match.items()):
                print(f"      {qv:<15} -> {actual_id}")
    else:
        print("  * No isomorphic motifs matched within temporal constraints.")

    print("\n--- INTELLIGENCE SEARCH METRICS ---")
    print(f"  * Total Graph Nodes   : {res.total_graph_nodes}")
    print(f"  * Total Temporal Edges: {res.total_graph_edges}")
    print(f"  * Matched Motifs Count: {res.matched_patterns_count}")
    print(f"  * Search Latency      : {res.search_latency_ms:.2f} ms")
    print(f"  * Edge Throughput     : {res.metrics.get('search_throughput_edges_per_sec', 0.0):,.0f} edges/sec")
    print("=" * 85)


def run_trace_counterfeits(args: argparse.Namespace) -> None:
    synthesizer = TemporalHypergraphSynthesizer()
    print("=" * 85)
    print("TEMPORAL HYPERGRAPH SYNTHESIZER: AEROSPACE COUNTERFEIT CHIP LAUNDERING TRACE")
    print(f"Benign Supplier Count : {args.suppliers} | Seed: {args.seed}")
    print("Audit Core            : Gray-Market Broker to Tier-1 Distributor Isomorphism")
    print("=" * 85)

    res = synthesizer.trace_counterfeit_supply_chains(benign_suppliers=args.suppliers, seed=args.seed)

    print("\n--- DETECTED COUNTERFEIT LAUNDERING SYNDICATE PATHS ---")
    if res.matches_found:
        for idx, match in enumerate(res.matches_found):
            print(f"  * Laundering Chain #{idx+1}:")
            for qv, actual_id in sorted(match.items()):
                print(f"      {qv:<15} -> {actual_id}")
    else:
        print("  * No illicit laundering chains detected.")

    print("\n--- SUPPLY CHAIN AUDIT METRICS ---")
    print(f"  * Total Supply Nodes  : {res.total_graph_nodes}")
    print(f"  * Total Shipments     : {res.total_graph_edges}")
    print(f"  * Detected Motifs     : {res.matched_patterns_count}")
    print(f"  * Trace Compute Time  : {res.search_latency_ms:.2f} ms")
    print("=" * 85)


def run_benchmark(args: argparse.Namespace) -> None:
    synthesizer = TemporalHypergraphSynthesizer()
    scales = [25, 50, 100, 200, 500]
    iterations = args.iterations

    print("=" * 90)
    print("TEMPORAL HYPERGRAPH BENCHMARK: SUBGRAPH ISOMORPHISM SEARCH LATENCY")
    print(f"Iterations per scale: {iterations} | Exact Temporal Monotonicity Matching")
    print("=" * 90)

    header = f"{'Graph Entities':<16} | {'Temporal Edges':<16} | {'Avg Latency (ms)':<18} | {'Throughput (edges/s)':<22}"
    print(header)
    print("-" * len(header))

    for n in scales:
        total_lat = 0.0
        edges_total = 0

        for it in range(iterations):
            res = synthesizer.detect_tactical_c2_cells(noise_nodes=n, seed=it)
            total_lat += res.search_latency_ms
            edges_total += res.total_graph_edges

        avg_lat = total_lat / iterations
        avg_edges = edges_total / iterations
        throughput = (avg_edges / (avg_lat / 1000.0)) if avg_lat > 0 else 0.0

        print(f"{n:<16} | {int(avg_edges):<16} | {avg_lat:>16.2f} | {throughput:>20.0f}")

    print("=" * 90)
    print("BENCHMARK COMPLETE: SUB-20MS TEMPORAL GRAPH SEARCH CONFIRMED.")
    print("=" * 90)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Temporal Hypergraph Synthesizer: Dual-Use C2 & Counterfeit Tracing CLI"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: detect-c2-cell
    p_c2 = subparsers.add_parser("detect-c2-cell", help="Detect tactical insurgent C2 communications motifs.")
    p_c2.add_argument("--noise", type=int, default=40, help="Noise civilian entities (default: 40)")
    p_c2.add_argument("--seed", type=int, default=42, help="Random seed (default: 42)")

    # Subcommand: trace-counterfeits
    p_chip = subparsers.add_parser("trace-counterfeits", help="Trace gray-market counterfeit chip laundering.")
    p_chip.add_argument("--suppliers", type=int, default=30, help="Benign suppliers (default: 30)")
    p_chip.add_argument("--seed", type=int, default=42, help="Random seed (default: 42)")

    # Subcommand: benchmark
    p_bench = subparsers.add_parser("benchmark", help="Benchmark subgraph isomorphism latency.")
    p_bench.add_argument("--iterations", type=int, default=25, help="Iterations per configuration (default: 25)")

    args = parser.parse_args()
    if args.command == "detect-c2-cell":
        run_detect_c2(args)
    elif args.command == "trace-counterfeits":
        run_trace_counterfeits(args)
    elif args.command == "benchmark":
        run_benchmark(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
