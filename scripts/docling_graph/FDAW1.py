import json
from pathlib import Path

import networkx as nx
import matplotlib.pyplot as plt


# --------------------------------------------------
# Paths
# --------------------------------------------------
JSON_FILE = "outputs/json_ocr/FDAW1.json"

GRAPH_IMAGE = (
    "outputs/docling_graph/FDAW1_docling_graph.png"
)

GRAPHML_FILE = (
    "outputs/docling_graph/FDAW1_docling_graph.graphml"
)


# --------------------------------------------------
# Main
# --------------------------------------------------
def main():

    # ----------------------------------------------
    # Load JSON
    # ----------------------------------------------
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("Texts:", len(data.get("texts", [])))
    print("Tables:", len(data.get("tables", [])))
    print("Pictures:", len(data.get("pictures", [])))
    print("Groups:", len(data.get("groups", [])))

    # ----------------------------------------------
    # Create Graph
    # ----------------------------------------------
    G = nx.DiGraph()

    # Root node
    G.add_node(
        "body",
        type="document_root"
    )

    # ----------------------------------------------
    # Add Text Nodes
    # ----------------------------------------------
    for idx, text_obj in enumerate(
        data.get("texts", [])
    ):

        text_content = text_obj.get(
            "text",
            ""
        )

        page_no = None

        if text_obj.get("prov"):

            page_no = (
                text_obj["prov"][0]
                .get("page_no")
            )

        G.add_node(
            f"text_{idx}",
            type="text",
            page=page_no,
            text=text_content[:200]
        )

        # body -> text
        G.add_edge(
            "body",
            f"text_{idx}",
            relation="contains"
        )

    # ----------------------------------------------
    # Add Group Nodes
    # ----------------------------------------------
    for idx, group_obj in enumerate(
        data.get("groups", [])
    ):

        group_node = f"group_{idx}"

        G.add_node(
            group_node,
            type="group",
            label=group_obj.get(
                "label",
                ""
            )
        )

        # body -> group
        G.add_edge(
            "body",
            group_node,
            relation="contains"
        )

        # group -> child nodes
        for child in group_obj.get(
            "children",
            []
        ):

            ref = child["$ref"]

            if ref.startswith(
                "#/texts/"
            ):

                text_idx = int(
                    ref.split("/")[-1]
                )

                G.add_edge(
                    group_node,
                    f"text_{text_idx}",
                    relation="contains"
                )

    # ----------------------------------------------
    # Add Picture Nodes
    # ----------------------------------------------
    for idx, picture_obj in enumerate(
        data.get("pictures", [])
    ):

        picture_node = (
            f"picture_{idx}"
        )

        page_no = None

        if picture_obj.get("prov"):

            page_no = (
                picture_obj["prov"][0]
                .get("page_no")
            )

        G.add_node(
            picture_node,
            type="picture",
            page=page_no
        )

        # body -> picture
        G.add_edge(
            "body",
            picture_node,
            relation="contains"
        )

        # picture -> child text
        for child in picture_obj.get(
            "children",
            []
        ):

            ref = child["$ref"]

            if ref.startswith(
                "#/texts/"
            ):

                text_idx = int(
                    ref.split("/")[-1]
                )

                G.add_edge(
                    picture_node,
                    f"text_{text_idx}",
                    relation="contains"
                )

    # ----------------------------------------------
    # Reading Order Links
    # ----------------------------------------------
    text_count = len(
        data.get("texts", [])
    )

    for i in range(
        text_count - 1
    ):

        G.add_edge(
            f"text_{i}",
            f"text_{i+1}",
            relation="next"
        )

    # ----------------------------------------------
    # Stats
    # ----------------------------------------------
    print(
        "\n===== GRAPH STATS ====="
    )

    print(
        "Nodes:",
        G.number_of_nodes()
    )

    print(
        "Edges:",
        G.number_of_edges()
    )

    # ----------------------------------------------
    # Save GraphML
    # ----------------------------------------------
    Path(
        "outputs/docling_graph"
    ).mkdir(
        parents=True,
        exist_ok=True
    )

    nx.write_graphml(
        G,
        GRAPHML_FILE
    )

    print(
        f"\nGraphML saved: "
        f"{GRAPHML_FILE}"
    )

    # ----------------------------------------------
    # Draw Graph
    # ----------------------------------------------
    plt.figure(
        figsize=(20, 15)
    )

    pos = nx.spring_layout(
        G,
        seed=42
    )

    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=500
    )

    nx.draw_networkx_edges(
        G,
        pos,
        arrows=True,
        alpha=0.5
    )

    nx.draw_networkx_labels(
        G,
        pos,
        font_size=6
    )

    plt.title(
        "FDAW1 Docling Graph"
    )

    plt.axis("off")

    plt.tight_layout()

    plt.savefig(
        GRAPH_IMAGE,
        dpi=300
    )

    print(
        f"Graph Image saved: "
        f"{GRAPH_IMAGE}"
    )

    plt.show()


if __name__ == "__main__":
    main()