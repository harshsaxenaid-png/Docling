from __future__ import annotations

import argparse
from pathlib import Path

from docling_graph import run_pipeline
from docling_graph.core import CypherExporter, PipelineConfig

from FDAW1_template import WarningLetter


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE = PROJECT_ROOT / "documents" / "FDAW1.pdf"
DEFAULT_OUTPUT = PROJECT_ROOT / "outputs" / "neo4j" / "graph.cypher"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the docling-graph FDAW1 pipeline and export graph.cypher."
    )
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--backend",
        choices=("llm", "vlm"),
        default="llm",
        help="docling-graph extraction backend.",
    )
    parser.add_argument(
        "--inference",
        choices=("local", "remote"),
        default="local",
        help="docling-graph inference mode.",
    )
    parser.add_argument(
        "--provider",
        default="ollama",
        help="Provider override. Defaults to the local Ollama provider.",
    )
    parser.add_argument(
        "--model",
        default="qwen2.5-coder:1.5b",
        help="Model override. Defaults to the locally running Ollama model.",
    )
    parser.add_argument(
        "--extraction-contract",
        choices=("direct", "staged", "delta"),
        default="direct",
    )
    parser.add_argument(
        "--no-structured-output",
        action="store_true",
        help="Disable schema-enforced structured output for models/providers that do not support it.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source = args.source.resolve()
    output_path = args.output.resolve()

    if not source.exists():
        raise FileNotFoundError(f"Source PDF not found: {source}")

    config = PipelineConfig(
        source=source,
        template=WarningLetter,
        backend=args.backend,
        inference=args.inference,
        extraction_contract=args.extraction_contract,
        model_override=args.model,
        provider_override=args.provider,
        structured_output=not args.no_structured_output,
        export_format="cypher",
        dump_to_disk=False,
    )

    context = run_pipeline(config)

    if context.knowledge_graph is None:
        raise RuntimeError("docling-graph did not return a knowledge graph")

    extracted_count = len(context.extracted_models or [])
    node_count = context.knowledge_graph.number_of_nodes()
    edge_count = context.knowledge_graph.number_of_edges()

    print(f"Number of extracted models: {extracted_count}")
    print(f"Number of graph nodes: {node_count}")
    print(f"Number of graph edges: {edge_count}")
    print(f"Graph Nodes: {node_count}")
    print(f"Graph Edges: {edge_count}")

    CypherExporter().export(context.knowledge_graph, output_path)
    print(f"Cypher Export Successful: {output_path}")


if __name__ == "__main__":
    main()
