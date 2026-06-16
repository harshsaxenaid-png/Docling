import json
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path


INPUT_FILE = "outputs/entity_relations/FDAW1_relations.json"
OUTPUT_FILE = "outputs/knowledge_graph/FDAW1_graph.png"


def main():

    # Load JSON
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    G = nx.DiGraph()

    # Add relations to graph
    for chunk in data:

        result = chunk.get("result", {})

        relations = result.get("relations", [])

        for rel in relations:

            source = rel.get("source")
            relation = rel.get("relation")
            target = rel.get("target")

            if source and target and relation:

                G.add_edge(
                    source,
                    target,
                    label=relation
                )

    print(f"Nodes: {G.number_of_nodes()}")
    print(f"Edges: {G.number_of_edges()}")

    # Create output folder
    Path("outputs/knowledge_graph").mkdir(
        parents=True,
        exist_ok=True
    )

    # Plot graph
    plt.figure(figsize=(20, 15))

    pos = nx.spring_layout(
        G,
        k=2,
        seed=42
    )

    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=3000,
        alpha=0.9
    )

    nx.draw_networkx_edges(
        G,
        pos,
        arrows=True,
        arrowsize=20
    )

    nx.draw_networkx_labels(
        G,
        pos,
        font_size=8
    )

    edge_labels = nx.get_edge_attributes(
        G,
        "label"
    )

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels,
        font_size=7
    )

    print("\nNodes:")
    for node in G.nodes():
      print(node)

    print("\nEdges:")
    for source, target, data in G.edges(data=True):
       print(
        f"{source} --{data['label']}--> {target}"
    )

    plt.title(
        "FDAW1 Knowledge Graph",
        fontsize=16
    )

    plt.axis("off")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_FILE,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    print(f"Graph saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()