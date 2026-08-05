#  -------------------------------------------------------------------------------------------------
#   Copyright (c) 2016-2025.  SupportVectors AI Lab
#   This code is part of the training material and, therefore, part of the intellectual property.
#   It may not be reused or shared without the explicit, written permission of SupportVectors.
#
#   Use is limited to the duration and purpose of the training at SupportVectors.
#
#   Author: SupportVectors AI Training Team
#  -------------------------------------------------------------------------------------------------
"""
Visualize GraphRAG output: interactive graph, community hierarchy, and summaries.

Usage:
  uv run python scripts/visualize_graphrag.py --root cmp_docs
  uv run python scripts/visualize_graphrag.py --root cmp_docs --no-browser

Outputs (under <root>/output/):
  - graphrag_graph.html   Interactive graph (nodes colored by community)
  - graphrag_communities.html   Community tree + summaries
  - graphrag_community_tree.html   Interactive tree of community titles (hover for summary)
"""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

import pandas as pd
import networkx as nx
from pyvis.network import Network


# Distinct colors for level-0 (root) communities; cycle through if there are more.
PALETTE = [
    "#e6194b", "#3cb44b", "#4363d8", "#f58231", "#911eb4",
    "#46f0f0", "#f032e6", "#bcf60c", "#fabebe", "#008080",
    "#e6beff", "#9a6324", "#fffac8", "#800000", "#aaffc3",
    "#808000", "#ffd8b1", "#000075", "#808080",
]


def load_data(root: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, nx.Graph]:
    """Load all GraphRAG index outputs from the project output directory.

    Reads parquet tables for entities, relationships, communities, and community
    reports, plus the GraphML graph. These are produced by the GraphRAG indexing
    pipeline and must exist before running this script.

    Args:
        root: Path to the GraphRAG project root (e.g. cmp_docs). Output files
            are read from root/output/.

    Returns:
        A 5-tuple of (entities, relationships, communities, reports, graph).
        - entities: DataFrame with entity id and title.
        - relationships: DataFrame of edges between entities.
        - communities: DataFrame with community id, parent, level, entity_ids, etc.
        - reports: DataFrame of community reports (title, summary, rank, rating_explanation, findings).
        - graph: NetworkX graph (GraphML) with nodes as entity titles.

    Raises:
        FileNotFoundError: If any required parquet or graph.graphml is missing.
    """
    out = root / "output"
    entities = pd.read_parquet(out / "entities.parquet")
    relationships = pd.read_parquet(out / "relationships.parquet")
    communities = pd.read_parquet(out / "communities.parquet")
    reports = pd.read_parquet(out / "community_reports.parquet")
    graph = nx.read_graphml(out / "graph.graphml")
    return entities, relationships, communities, reports, graph


def build_entity_id_to_title(entities: pd.DataFrame) -> dict[str, str]:
    """Build a mapping from entity id (as string) to entity title.

    Used to resolve entity ids in community membership to human-readable labels
    for graph tooltips and community display.

    Args:
        entities: DataFrame with columns "id" and "title".

    Returns:
        Dict mapping string entity id to title.
    """
    return dict(zip(entities["id"].astype(str), entities["title"].astype(str)))


def _resolve_root_community(
    cid: int,
    comm_df: pd.DataFrame,
    root_of: dict[int, int],
) -> int:
    """Resolve the root (level-0) community id for a given community id.

    Walks the parent chain until a community with parent == -1 is found.
    Results are memoized in root_of so each community is resolved only once.

    Args:
        cid: Community id to resolve.
        comm_df: Communities DataFrame with "community" and "parent" columns.
        root_of: Mutable dict to cache cid -> root_community_id. Updated in place.

    Returns:
        The root community id for cid.
    """
    if cid in root_of:
        return root_of[cid]
    rows = comm_df[comm_df["community"] == cid]
    p = int(rows["parent"].iloc[0]) if len(rows) else -1
    if p == -1:
        root_of[cid] = cid
        return cid
    r = _resolve_root_community(p, comm_df, root_of)
    root_of[cid] = r
    return r


def build_entity_to_root_community(
    communities: pd.DataFrame,
    entity_id_to_title: dict[str, str],
) -> dict[str, int]:
    """Map each entity title to its root (level-0) community id for graph coloring.

    Entities may belong to nested communities; this assigns each entity to the
    top-level community in that hierarchy. Used so all nodes in the same
    root community share one color in the interactive graph.

    Args:
        communities: DataFrame with community, parent, level, entity_ids.
        entity_id_to_title: Mapping from entity id string to title (from
            build_entity_id_to_title).

    Returns:
        Dict mapping entity title to root community id (int). Only the first
        community containing an entity is recorded when an entity appears
        in multiple communities.
    """
    comm_df = communities.copy()
    comm_df["community"] = comm_df["community"].astype(int)
    comm_df["parent"] = comm_df["parent"].astype(int)
    root_of: dict[int, int] = {}

    # Resolve root community for every community id (fills root_of cache).
    for cid in comm_df["community"].unique():
        _resolve_root_community(cid, comm_df, root_of)

    # Map entity title -> root community id using first community that contains it.
    title_to_root: dict[str, int] = {}
    for _, row in comm_df.iterrows():
        cid = int(row["community"])
        root_cid = root_of.get(cid, cid)
        eids = row["entity_ids"]
        if eids is not None and len(eids):
            for eid in list(eids):
                eid_str = str(eid)
                if eid_str in entity_id_to_title:
                    title = entity_id_to_title[eid_str]
                    if title not in title_to_root:
                        title_to_root[title] = root_cid
    return title_to_root


def build_community_tree(communities: pd.DataFrame) -> list[dict]:
    """Build a hierarchical tree of communities for the communities HTML page.

    Converts the flat communities table (with parent pointers) into a tree of
    dicts with "community", "level", "title", "size", and "children". Root
    communities have no parent; others are nested under their parent.

    Args:
        communities: DataFrame with community, parent, level, title, size, entity_ids.

    Returns:
        List of root nodes. Each node is a dict with keys: community, level,
        title, size, children (list of child nodes). Roots and children are
        sorted by community id.
    """
    comm_df = communities.copy()
    comm_df["community"] = comm_df["community"].astype(int)
    comm_df["parent"] = comm_df["parent"].astype(int)
    by_id: dict[int, dict] = {}

    # One node per community.
    for _, row in comm_df.iterrows():
        cid = int(row["community"])
        by_id[cid] = {
            "community": cid,
            "level": int(row["level"]),
            "title": str(row["title"]) if pd.notna(row["title"]) else f"Community {cid}",
            "size": int(row["size"]) if pd.notna(row["size"]) else 0,
            "children": [],
        }

    # Attach each node to its parent (or collect roots).
    roots: list[dict] = []
    for cid, node in by_id.items():
        parent = int(comm_df[comm_df["community"] == cid]["parent"].iloc[0])
        if parent == -1:
            roots.append(node)
        else:
            by_id[parent]["children"].append(node)

    # Stable order for display.
    roots.sort(key=lambda n: n["community"])
    for node in by_id.values():
        node["children"].sort(key=lambda n: n["community"])
    return roots


def generate_graph_html(
    graph: nx.Graph,
    entity_to_community: dict[str, int],
    reports: pd.DataFrame,
    out_path: Path,
) -> None:
    """Generate an interactive Pyvis graph HTML with nodes colored by root community.

    Nodes are entity titles; edges come from the graph. Each node is colored
    by its root community (from entity_to_community) and shows a tooltip with
    the community report title and summary.

    Args:
        graph: NetworkX graph (nodes = entity titles, edges may have "weight").
        entity_to_community: Map from entity title to root community id (from
            build_entity_to_root_community).
        reports: Community reports DataFrame (community, title, summary).
        out_path: Path to write the HTML file (e.g. output/graphrag_graph.html).
    """
    # Precompute a seed layout so physics starts from a sensible position.
    try:
        pos = nx.spring_layout(graph, k=0.5, iterations=50, seed=42)
    except Exception:
        pos = nx.shell_layout(graph) if graph.nodes() else {}
    # Scale to a reasonable canvas range (vis-network uses roughly -500..500 by default).
    if pos:
        xs = [pos[n][0] for n in pos]
        ys = [pos[n][1] for n in pos]
        x_min, x_max = min(xs), max(xs)
        y_min, y_max = min(ys), max(ys)
        x_span = x_max - x_min or 1
        y_span = y_max - y_min or 1
        scale = 800
        pos = {
            n: (
                ((pos[n][0] - x_min) / x_span - 0.5) * scale,
                ((pos[n][1] - y_min) / y_span - 0.5) * scale,
            )
            for n in pos
        }
    else:
        pos = {}

    # Pyvis Network: remote CDN so the HTML works when opened as file://.
    net = Network(
        height="800px",
        width="100%",
        bgcolor="#1a1a2e",
        font_color="#eee",
        select_menu=True,
        filter_menu=True,
        cdn_resources="remote",
    )
    # Keep physics enabled so users can drag and rearrange nodes interactively.
    net.set_options("""
    var options = {
      "nodes": {
        "font": { "size": 12 },
        "borderWidth": 1,
        "borderWidthSelected": 2
      },
      "edges": {
        "color": { "inherit": "both" },
        "smooth": { "type": "continuous" }
      },
      "physics": {
        "enabled": true,
        "solver": "forceAtlas2Based",
        "forceAtlas2Based": {
          "gravitationalConstant": -45,
          "centralGravity": 0.01,
          "springLength": 120,
          "springConstant": 0.08
        },
        "stabilization": {
          "enabled": true,
          "iterations": 300,
          "updateInterval": 25
        }
      },
      "interaction": {
        "hover": true,
        "tooltipDelay": 100,
        "multiselect": true,
        "dragNodes": true,
        "dragView": true,
        "zoomView": true,
        "navigationButtons": true
      }
    }
    """)

    # Build community id -> {title, summary} from reports (first row per community).
    report_by_comm: dict[int, dict] = {}
    for _, row in reports.iterrows():
        cid = int(row["community"])
        if cid not in report_by_comm:
            summary = str(row["summary"]) if pd.notna(row["summary"]) else ""
            if len(summary) > 300:
                summary = summary[:300] + "..."
            report_by_comm[cid] = {
                "title": str(row["title"]) if pd.notna(row["title"]) else f"Community {cid}",
                "summary": summary,
            }

    # Assign a color to each root community that appears in the graph.
    root_communities = sorted(set(entity_to_community.values()))
    color_by_comm = {cid: PALETTE[i % len(PALETTE)] for i, cid in enumerate(root_communities)}

    # Add nodes: color by root community, tooltip from report, precomputed position.
    for node_id in graph.nodes():
        comm_id = entity_to_community.get(node_id)
        if comm_id is None:
            color = "#666"
            title = node_id
        else:
            color = color_by_comm.get(comm_id, "#666")
            rep = report_by_comm.get(comm_id, {})
            report_title = rep.get("title", f"Community {comm_id}")
            report_summary = rep.get("summary", "")
            title = f"<b>{html.escape(node_id)}</b><br/>Community: {html.escape(report_title)}<br/>{html.escape(report_summary)}"
        label = node_id[:30] + "…" if len(node_id) > 32 else node_id
        node_opts = {"label": label, "title": title, "color": color, "physics": True}
        if node_id in pos:
            node_opts["x"] = pos[node_id][0]
            node_opts["y"] = pos[node_id][1]
        net.add_node(node_id, **node_opts)

    # Add edges (optionally show weight in tooltip).
    for u, v, data in graph.edges(data=True):
        w = data.get("weight", 1.0)
        net.add_edge(u, v, value=float(w), title=f"Weight: {w}")

    net.save_graph(str(out_path))


def _normalize_findings(findings: list | str | float | None) -> list[dict[str, str]]:
    """Normalize report findings to a structured list suitable for JSON payloads."""
    if findings is None or (isinstance(findings, float) and pd.isna(findings)):
        return []
    if isinstance(findings, str):
        stripped = findings.strip()
        if not stripped:
            return []
        try:
            findings = json.loads(stripped)
        except Exception:
            return [{"summary": stripped, "explanation": ""}]

    if not isinstance(findings, list):
        return []

    normalized: list[dict[str, str]] = []
    for entry in findings[:12]:
        if isinstance(entry, dict):
            normalized.append(
                {
                    "summary": str(entry.get("summary", "")),
                    "explanation": str(entry.get("explanation", "")),
                }
            )
        else:
            normalized.append({"summary": str(entry), "explanation": ""})
    return normalized


def _community_tree_payload(node: dict, report_by_comm: dict[int, dict]) -> dict:
    """Convert a community tree node to a JSON-friendly payload for UI rendering."""
    cid = int(node["community"])
    row = report_by_comm.get(cid, {})
    summary = str(row.get("summary", "") or "")
    rating = row.get("rank")
    if rating is not None and isinstance(rating, float) and pd.isna(rating):
        rating = None

    return {
        "id": cid,
        "level": int(node.get("level", 0)),
        "title": str(row.get("title") or node.get("title") or f"Community {cid}"),
        "size": int(node.get("size", 0)),
        "summary": summary,
        "rating": rating,
        "rating_explanation": str(row.get("rating_explanation", "") or ""),
        "findings": _normalize_findings(row.get("findings")),
        "children": [
            _community_tree_payload(child, report_by_comm)
            for child in node.get("children", [])
        ],
    }


def _count_tree_nodes(nodes: list[dict]) -> int:
    """Count total nodes in a nested community tree payload."""
    return sum(1 + _count_tree_nodes(node.get("children", [])) for node in nodes)


def generate_communities_html(
    tree: list[dict],
    reports: pd.DataFrame,
    out_path: Path,
) -> None:
    """Generate an interactive community hierarchy page with side-panel metadata."""
    report_by_comm = reports.set_index("community").to_dict("index")
    tree_data = [_community_tree_payload(node, report_by_comm) for node in tree]
    total_nodes = _count_tree_nodes(tree_data)
    payload = json.dumps(tree_data, ensure_ascii=False).replace("</script>", "<\\/script>")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>GraphRAG Communities &amp; Summaries</title>
  <style>
    :root {{
      color-scheme: light dark;
      --bg: #0f172a;
      --bg-soft: #111827;
      --card: #1f2937;
      --muted: #9ca3af;
      --text: #f9fafb;
      --accent: #60a5fa;
      --leaf: #34d399;
      --border: #334155;
      --chip: #1e293b;
      --chip-border: #475569;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: radial-gradient(circle at top, #1e293b 0%, #0f172a 45%);
      color: var(--text);
      font: 14px/1.5 Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      min-height: 100vh;
    }}
    .container {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 28px 20px 48px;
      display: grid;
      gap: 18px;
      grid-template-columns: minmax(280px, 1fr) minmax(280px, 440px);
    }}
    .header {{
      grid-column: 1 / -1;
      background: linear-gradient(120deg, rgba(96,165,250,0.18), rgba(52,211,153,0.12));
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 18px;
    }}
    h1 {{ margin: 0 0 6px; font-size: 22px; letter-spacing: 0.2px; }}
    .stats {{ margin: 0; color: var(--muted); font-size: 13px; }}
    .panel {{
      background: rgba(17,24,39,0.84);
      border: 1px solid var(--border);
      border-radius: 14px;
      overflow: hidden;
      min-height: 320px;
      backdrop-filter: blur(3px);
    }}
    .panel h2 {{
      margin: 0;
      padding: 12px 14px;
      border-bottom: 1px solid var(--border);
      font-size: 14px;
      font-weight: 700;
      color: #cbd5e1;
      background: rgba(15, 23, 42, 0.5);
    }}
    .tree-wrap {{ padding: 12px 14px 16px; overflow: auto; max-height: 75vh; }}
    ul.tree {{ margin: 0; padding-left: 14px; list-style: none; }}
    ul.tree ul {{ list-style: none; margin: 0; padding-left: 18px; border-left: 1px dashed #334155; }}
    .node-row {{
      display: flex;
      align-items: center;
      gap: 8px;
      margin: 7px 0;
    }}
    .toggle {{
      width: 20px;
      height: 20px;
      border-radius: 999px;
      border: 1px solid var(--chip-border);
      background: var(--chip);
      color: #cbd5e1;
      cursor: pointer;
      font-size: 12px;
      line-height: 18px;
      padding: 0;
    }}
    .toggle.empty {{
      visibility: hidden;
      pointer-events: none;
    }}
    .node-btn {{
      border: 1px solid var(--border);
      background: rgba(15, 23, 42, 0.7);
      color: var(--text);
      border-radius: 10px;
      padding: 6px 9px;
      cursor: pointer;
      text-align: left;
      width: 100%;
      transition: 140ms ease;
    }}
    .node-btn:hover {{ border-color: var(--accent); transform: translateY(-1px); }}
    .node-btn.active {{ outline: 1px solid var(--accent); border-color: var(--accent); }}
    .meta {{
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
      margin-top: 5px;
      font-size: 11px;
      color: var(--muted);
    }}
    .chip {{
      border: 1px solid var(--chip-border);
      background: var(--chip);
      border-radius: 999px;
      padding: 2px 7px;
    }}
    .chip.root {{
      border-color: rgba(52,211,153,0.5);
      color: var(--leaf);
    }}
    .chip.nested {{
      border-color: rgba(96,165,250,0.5);
      color: var(--accent);
    }}
    .details {{
      padding: 14px;
      display: grid;
      gap: 12px;
      max-height: 75vh;
      overflow: auto;
    }}
    .card {{
      border: 1px solid var(--border);
      background: rgba(15, 23, 42, 0.55);
      border-radius: 12px;
      padding: 12px;
    }}
    .card h3 {{
      margin: 0 0 8px;
      font-size: 13px;
      color: #cbd5e1;
      text-transform: uppercase;
      letter-spacing: 0.6px;
    }}
    .summary-text {{
      margin: 0;
      white-space: pre-wrap;
      color: #e5e7eb;
      line-height: 1.55;
    }}
    .list {{
      margin: 0;
      padding-left: 18px;
      color: #e5e7eb;
    }}
    .list li {{ margin: 6px 0; }}
    .hint {{ margin: 0; color: var(--muted); font-size: 13px; }}
    .finding-summary {{ font-weight: 700; color: #f3f4f6; }}
    .finding-explanation {{ color: #cbd5e1; margin-top: 2px; }}
    @media (max-width: 980px) {{
      .container {{ grid-template-columns: 1fr; }}
      .tree-wrap, .details {{ max-height: none; }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <section class="header">
      <h1>GraphRAG Communities &amp; Summaries</h1>
      <p class="stats">Total communities: {total_nodes} | Root communities: {len(tree_data)} | Click a community to inspect details.</p>
    </section>

    <section class="panel">
      <h2>Community Hierarchy</h2>
      <div class="tree-wrap">
        <div id="tree-root"></div>
      </div>
    </section>

    <section class="panel">
      <h2>Community Metadata</h2>
      <div class="details" id="details-panel">
        <p class="hint">Select any community in the tree to view summary, rating, and findings.</p>
      </div>
    </section>
  </div>
  <script>
    const treeData = {payload};
    const treeRoot = document.getElementById("tree-root");
    const detailsPanel = document.getElementById("details-panel");
    let activeButton = null;

    function preview(text, max = 110) {{
      if (!text) return "(no summary)";
      const collapsed = String(text).replace(/\\s+/g, " ").trim();
      if (collapsed.length <= max) return collapsed;
      return collapsed.slice(0, max) + " ...";
    }}

    function escapeHtml(value) {{
      return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
    }}

    function findingsHtml(findings) {{
      if (!Array.isArray(findings) || findings.length === 0) {{
        return '<p class="hint">No findings for this community.</p>';
      }}
      const items = findings.map((item) => {{
        const summary = escapeHtml(item.summary || "");
        const explanation = escapeHtml(item.explanation || "");
        return `<li>
          <div class="finding-summary">${{summary || "(no summary)"}}</div>
          ${{explanation ? `<div class="finding-explanation">${{explanation}}</div>` : ""}}
        </li>`;
      }}).join("");
      return `<ol class="list">${{items}}</ol>`;
    }}

    function setDetails(node) {{
      const childIds = (node.children || []).map((child) => `<li>${{escapeHtml(String(child.id))}}</li>`).join("");
      const ratingText = node.rating == null ? "N/A" : escapeHtml(String(node.rating));
      const ratingExpl = node.rating_explanation ? escapeHtml(node.rating_explanation) : "No rating explanation provided.";
      detailsPanel.innerHTML = `
        <article class="card">
          <h3>Identity</h3>
          <p class="summary-text"><strong>Community ID:</strong> ${{escapeHtml(String(node.id))}}</p>
          <p class="summary-text"><strong>Level:</strong> ${{escapeHtml(String(node.level))}}</p>
          <p class="summary-text"><strong>Size:</strong> ${{escapeHtml(String(node.size))}}</p>
          <p class="summary-text"><strong>Type:</strong> ${{node.level === 0 ? "Root community" : "Nested community"}}</p>
        </article>
        <article class="card">
          <h3>Title</h3>
          <p class="summary-text">${{escapeHtml(node.title || "")}}</p>
        </article>
        <article class="card">
          <h3>Summary</h3>
          <p class="summary-text">${{escapeHtml(node.summary || "") || "No summary available."}}</p>
        </article>
        <article class="card">
          <h3>Rating</h3>
          <p class="summary-text"><strong>Impact rank:</strong> ${{ratingText}}</p>
          <p class="summary-text"><strong>Explanation:</strong> ${{ratingExpl}}</p>
        </article>
        <article class="card">
          <h3>Findings (${{(node.findings || []).length}})</h3>
          ${{findingsHtml(node.findings)}}
        </article>
        <article class="card">
          <h3>Child Community IDs (${{(node.children || []).length}})</h3>
          ${{childIds ? `<ul class="list">${{childIds}}</ul>` : '<p class="hint">No children (leaf community).</p>'}}
        </article>
      `;
    }}

    function makeNodeElement(node, startCollapsed = true) {{
      const li = document.createElement("li");
      const row = document.createElement("div");
      row.className = "node-row";

      const hasChildren = (node.children || []).length > 0;
      const toggle = document.createElement("button");
      toggle.className = "toggle" + (hasChildren ? "" : " empty");
      toggle.type = "button";
      toggle.textContent = hasChildren ? (startCollapsed ? "+" : "-") : " ";
      row.appendChild(toggle);

      const nodeButton = document.createElement("button");
      nodeButton.type = "button";
      nodeButton.className = "node-btn";
      nodeButton.innerHTML = `
        <div><strong>#${{escapeHtml(String(node.id))}}</strong> ${{escapeHtml(preview(node.title || node.summary))}}</div>
        <div class="meta">
          <span class="chip">${{node.level}}</span>
          <span class="chip ${{node.level === 0 ? "root" : "nested"}}">${{node.level === 0 ? "root" : "nested"}}</span>
          <span class="chip">size: ${{node.size}}</span>
          <span class="chip">children: ${{(node.children || []).length}}</span>
          <span class="chip">findings: ${{(node.findings || []).length}}</span>
        </div>
      `;
      nodeButton.addEventListener("click", () => {{
        if (activeButton) activeButton.classList.remove("active");
        nodeButton.classList.add("active");
        activeButton = nodeButton;
        setDetails(node);
      }});
      row.appendChild(nodeButton);
      li.appendChild(row);

      const childrenContainer = document.createElement("ul");
      childrenContainer.className = "tree";
      childrenContainer.style.display = startCollapsed ? "none" : "block";
      (node.children || []).forEach((child) => {{
        childrenContainer.appendChild(makeNodeElement(child, true));
      }});
      li.appendChild(childrenContainer);

      if (hasChildren) {{
        toggle.addEventListener("click", () => {{
          const isCollapsed = childrenContainer.style.display === "none";
          childrenContainer.style.display = isCollapsed ? "block" : "none";
          toggle.textContent = isCollapsed ? "-" : "+";
        }});
      }}

      return li;
    }}

    function renderTree() {{
      const ul = document.createElement("ul");
      ul.className = "tree";
      treeData.forEach((rootNode) => {{
        ul.appendChild(makeNodeElement(rootNode, false));
      }});
      treeRoot.appendChild(ul);
    }}

    renderTree();
  </script>
</body>
</html>
"""
    out_path.write_text(html_content, encoding="utf-8")


def _tree_to_d3_node(node: dict, report_by_comm: dict[int, dict]) -> dict:
    """Convert internal community tree node to D3 hierarchy node (name, id, summary, children)."""
    cid = node["community"]
    row = report_by_comm.get(cid, {})
    title = row.get("title") or node.get("title") or f"Community {cid}"
    summary = row.get("summary") or ""
    d3_node = {
        "name": f"{title} (id={cid})",
        "id": cid,
        "summary": summary,
        "children": [_tree_to_d3_node(ch, report_by_comm) for ch in node["children"]],
    }
    # D3 hierarchy expects children only when non-empty
    if not d3_node["children"]:
        del d3_node["children"]
    return d3_node


def generate_community_tree_viz_html(
    tree: list[dict],
    reports: pd.DataFrame,
    out_path: Path,
) -> None:
    """Generate an HTML page with a D3 tree of community titles (id); hover shows summary.

    Args:
        tree: List of root nodes from build_community_tree.
        reports: Community reports DataFrame (community, title, summary, ...).
        out_path: Path to write the HTML file (e.g. output/graphrag_community_tree.html).
    """
    report_by_comm = reports.set_index("community").to_dict("index")
    d3_roots = [_tree_to_d3_node(n, report_by_comm) for n in tree]
    # Single root for D3 hierarchy
    root_data = {"name": "Communities", "id": None, "summary": "", "children": d3_roots}
    # Embed as JSON; escape </script> so it doesn't close the script tag
    data_json = json.dumps(root_data, ensure_ascii=False)
    data_json_escaped = data_json.replace("</script>", "<\\/script>")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>GraphRAG Community Tree</title>
  <script src="https://d3js.org/d3.v7.min.js"></script>
  <style>
    :root {{ --bg: #0f0f1a; --card: #1a1a2e; --text: #e0e0e0; --accent: #6366f1; --link: #a5b4fc; --muted: #888; }}
    html, body {{ height: 100%; margin: 0; overflow: hidden; }}
    body {{ font-family: system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); display: flex; flex-direction: column; }}
    .top-pane {{ flex-shrink: 0; padding: 1rem 1rem 0.5rem; background: var(--bg); border-bottom: 1px solid #333; }}
    .top-pane h1 {{ margin: 0 0 0.25rem; color: #fff; }}
    .top-pane p {{ margin: 0 0 0.75rem; font-size: 0.9rem; color: var(--muted); }}
    .controls {{ display: flex; flex-wrap: wrap; gap: 1rem; align-items: flex-end; padding: 0.75rem; background: var(--card); border-radius: 8px; border: 1px solid #333; }}
    .controls label {{ display: flex; flex-direction: column; gap: 0.25rem; font-size: 0.9rem; color: var(--muted); }}
    .controls select, .controls input {{ padding: 0.4rem 0.6rem; background: var(--bg); border: 1px solid #444; border-radius: 4px; color: var(--text); min-width: 140px; }}
    .controls button {{ padding: 0.5rem 1rem; background: var(--accent); color: #fff; border: none; border-radius: 4px; cursor: pointer; font-size: 0.9rem; }}
    .controls button:hover {{ filter: brightness(1.1); }}
    #tree-container {{ flex: 1; min-height: 0; width: 100%; cursor: grab; }}
    #tree-container:active {{ cursor: grabbing; }}
    .node circle {{ fill: var(--card); stroke: var(--accent); stroke-width: 2px; cursor: pointer; }}
    .node:hover circle {{ stroke: #a5b4fc; stroke-width: 3px; }}
    .node text {{ font-size: 12px; fill: var(--text); pointer-events: none; }}
    .link {{ fill: none; stroke: #444; stroke-width: 1.5px; }}
    .tooltip {{ position: absolute; padding: 10px 14px; background: var(--card); border: 1px solid var(--accent); border-radius: 8px; max-width: 400px; max-height: 300px; overflow-y: auto; font-size: 13px; line-height: 1.5; box-shadow: 0 4px 20px rgba(0,0,0,0.4); pointer-events: none; z-index: 1000; }}
  </style>
</head>
<body>
  <div class="top-pane">
    <h1>GraphRAG Community Tree</h1>
    <p>Tree of community titles and IDs. Hover for summary. <strong>Drag a node</strong> to separate labels; <strong>double-click</strong> to zoom to node. Drag background to pan, scroll to zoom.</p>
    <div class="controls">
      <label>
        Max level
        <select id="filter-level" title="Show only communities up to this depth (0 = root, 1 = first sub-level, etc.)">
          <option value="all">All levels</option>
        </select>
      </label>
      <label>
        Start from (id or title)
        <input type="text" id="filter-id-title" placeholder="e.g. 5 or RAG" title="Show only this community and its sub-communities (match by id or title substring)" />
      </label>
      <button type="button" id="apply-filters">Apply filters</button>
    </div>
  </div>
  <div id="tree-container"></div>
  <div id="tooltip" class="tooltip" style="display: none;"></div>

  <script>
(function() {{
  const rootData = {data_json_escaped};
  const fullRoot = d3.hierarchy(rootData, d => d.children);
  const maxDepthGlobal = fullRoot.height;

  const dx = 22;
  const dy = 140;
  const treeLayout = d3.tree().nodeSize([dx, dy]);
  const pad = 40;

  const levelSelect = document.getElementById("filter-level");
  for (let i = 0; i <= maxDepthGlobal; i++) levelSelect.appendChild(new Option(String(i), String(i)));

  function toData(node) {{
    return {{ name: node.data.name, id: node.data.id, summary: node.data.summary, children: node.children && node.children.length ? node.children.map(toData) : undefined }};
  }}
  function pruneToDepth(node, maxDepth) {{
    if (node.depth > maxDepth) return null;
    const children = node.children ? node.children.map(c => pruneToDepth(c, maxDepth)).filter(Boolean) : undefined;
    return {{ name: node.data.name, id: node.data.id, summary: node.data.summary, children: children && children.length ? children : undefined }};
  }}
  function getDisplayRoot() {{
    const levelVal = levelSelect.value;
    const idTitle = (document.getElementById("filter-id-title").value || "").trim();
    let displayRoot;
    if (idTitle) {{
      const match = fullRoot.descendants().find(d => {{
        if (d.data.id != null && String(d.data.id) === idTitle) return true;
        if (d.data.name && d.data.name.toLowerCase().includes(idTitle.toLowerCase())) return true;
        return false;
      }});
      if (!match) {{ alert("No community found matching '" + idTitle + "'. Try an id (e.g. 5) or part of a title."); return null; }}
      displayRoot = d3.hierarchy(toData(match), d => d.children);
    }} else {{
      displayRoot = d3.hierarchy(rootData, d => d.children);
    }}
    if (levelVal !== "all") {{
      const maxD = parseInt(levelVal, 10);
      const pruned = pruneToDepth(displayRoot, maxD);
      if (!pruned) return null;
      displayRoot = d3.hierarchy(pruned, d => d.children);
    }}
    return displayRoot;
  }}

  let viewWidth = 800, viewHeight = 600, treeOffsetX = 0, treeOffsetY = 0;
  const container = document.getElementById("tree-container");
  const svg = d3.select("#tree-container")
    .append("svg")
    .attr("width", "100%")
    .attr("height", "100%")
    .attr("preserveAspectRatio", "xMidYMid meet")
    .style("display", "block");
  const zoomG = svg.append("g").attr("class", "zoom-group");
  const treeG = zoomG.append("g").attr("class", "tree-content");

  const zoom = d3.zoom()
    .scaleExtent([0.2, 4])
    .filter((event) => !event.target.closest(".node"))
    .on("zoom", (event) => zoomG.attr("transform", event.transform));
  svg.call(zoom);

  const tooltipEl = document.getElementById("tooltip");
  function attachNodeBehaviors(linkSel, nodeSel) {{
    function redrawLinks() {{ linkSel.attr("d", d3.linkHorizontal().x(d => d.y).y(d => d.x)); }}
    const drag = d3.drag()
      .subject((event, d) => ({{ x: d.y, y: d.x }}))
      .on("drag", function(event, d) {{
        d.y = event.x;
        d.x = event.y;
        d3.select(this).attr("transform", `translate(${{d.y}}, ${{d.x}})`);
        redrawLinks();
      }});
    nodeSel.call(drag);
    nodeSel.on("dblclick", function(event, d) {{
      event.stopPropagation();
      const px = treeOffsetX + d.y;
      const py = treeOffsetY + d.x;
      const w = container.clientWidth || viewWidth;
      const h = container.clientHeight || viewHeight;
      const k = 1.8;
      svg.transition().duration(300).call(zoom.transform, d3.zoomIdentity.translate(w / 2 - k * px, h / 2 - k * py).scale(k));
    }});
    nodeSel.on("mouseenter", function(event, d) {{
      if (d.data.summary == null || d.data.summary === "") return;
      tooltipEl.textContent = d.data.summary;
      tooltipEl.style.display = "block";
      tooltipEl.style.left = (event.pageX + 12) + "px";
      tooltipEl.style.top = (event.pageY + 12) + "px";
    }});
    nodeSel.on("mousemove", function(event) {{
      tooltipEl.style.left = (event.pageX + 12) + "px";
      tooltipEl.style.top = (event.pageY + 12) + "px";
    }});
    nodeSel.on("mouseleave", () => {{ tooltipEl.style.display = "none"; }});
  }}

  function fitToView() {{
    const w = container.clientWidth || viewWidth;
    const h = container.clientHeight || viewHeight;
    const s = Math.min(w / viewWidth, h / viewHeight, 1);
    const tx = viewWidth * (1 - s) / 2;
    const ty = viewHeight * (1 - s) / 2;
    svg.call(zoom.transform, d3.zoomIdentity.translate(tx, ty).scale(s));
  }}

  function renderTree(displayRoot) {{
    treeLayout(displayRoot);
    let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
    displayRoot.each(d => {{
      if (d.x > x1) x1 = d.x;
      if (d.x < x0) x0 = d.x;
      if (d.y > y1) y1 = d.y;
      if (d.y < y0) y0 = d.y;
    }});
    const contentWidth = y1 - y0;
    const contentHeight = x1 - x0;
    viewWidth = contentWidth + 2 * pad;
    viewHeight = contentHeight + 2 * pad;
    treeOffsetX = pad - y0;
    treeOffsetY = pad - x0;

    svg.attr("viewBox", [0, 0, viewWidth, viewHeight]);
    treeG.attr("transform", `translate(${{treeOffsetX}}, ${{treeOffsetY}})`);

    const link = treeG.selectAll(".link").data(displayRoot.links()).join("path").attr("class", "link").attr("d", d3.linkHorizontal().x(d => d.y).y(d => d.x));
    const node = treeG.selectAll(".node").data(displayRoot.descendants()).join("g").attr("class", "node").attr("transform", d => `translate(${{d.y}}, ${{d.x}})`);
    node.selectAll("circle").remove();
    node.selectAll("text").remove();
    node.filter(d => d.depth > 0).append("circle").attr("r", 4.5);
    node.append("text").attr("dy", "0.32em").attr("x", d => d.children ? -8 : 8).attr("text-anchor", d => d.children ? "end" : "start").text(d => d.data.name);

    attachNodeBehaviors(link, node);
    fitToView();
  }}

  function applyFilters() {{
    const displayRoot = getDisplayRoot();
    if (displayRoot) renderTree(displayRoot);
  }}
  document.getElementById("apply-filters").addEventListener("click", applyFilters);
  document.getElementById("filter-id-title").addEventListener("keydown", function(e) {{ if (e.key === "Enter") applyFilters(); }});
  levelSelect.addEventListener("change", applyFilters);

  renderTree(fullRoot);
  window.addEventListener("resize", fitToView);
}})();
  </script>
</body>
</html>
"""
    out_path.write_text(html_content, encoding="utf-8")


def main() -> None:
    """CLI entry point: load GraphRAG output, generate graph and communities HTML, optionally open in browser."""
    parser = argparse.ArgumentParser(description="Visualize GraphRAG graph, communities, and summaries")
    parser.add_argument("--root", type=Path, default=Path("cmp_docs"), help="GraphRAG project root (e.g. cmp_docs)")
    parser.add_argument("--no-browser", action="store_true", help="Do not open HTML files in browser")
    args = parser.parse_args()
    root = args.root.resolve()

    if not (root / "output" / "graph.graphml").exists():
        raise SystemExit(f"Not found: {root}/output/graph.graphml. Run graphrag index first.")

    entities, _, communities, reports, graph = load_data(root)
    entity_id_to_title = build_entity_id_to_title(entities)
    entity_to_community = build_entity_to_root_community(communities, entity_id_to_title)
    tree = build_community_tree(communities)

    out_dir = root / "output"
    graph_path = out_dir / "graphrag_graph.html"
    communities_path = out_dir / "graphrag_communities.html"
    community_tree_path = out_dir / "graphrag_community_tree.html"

    generate_graph_html(graph, entity_to_community, reports, graph_path)
    generate_communities_html(tree, reports, communities_path)
    generate_community_tree_viz_html(tree, reports, community_tree_path)

    print("Generated:")
    print(f"  Graph:        {graph_path}")
    print(f"  Communities:  {communities_path}")
    print(f"  Community tree: {community_tree_path}")
    if not args.no_browser:
        import webbrowser
        webbrowser.open(graph_path.as_uri())
        webbrowser.open(communities_path.as_uri())
        webbrowser.open(community_tree_path.as_uri())


if __name__ == "__main__":
    main()
