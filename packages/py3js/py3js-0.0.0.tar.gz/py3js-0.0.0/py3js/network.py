from importlib import resources
import json
from typing import List


class Node:
    def __init__(self, name: str, tooltip: str = None, color: str = None):
        self.name = name
        self.tooltip = tooltip
        self.color = color


class Link:
    def __init__(self, source: str, target: str, color: str = "black", fill: str = "black"):
        self.source = source
        self.target = target
        self.color = color
        self.fill = fill


class ForceDirectedGraph:

    def __init__(self, width: int = 800, height: int = 600):
        self._html = resources.read_text("py3js", "force.html")
        self._html = (self._html
                      .replace("$width", str(width))
                      .replace("$height", str(height)))

        self._nodes: List[Node] = []
        self._links: List[Link] = []

    def add_node(self, node: Node):
        self._nodes.append(node)

    def add_link(self, link: Link):
        self._links.append(link)

    def _render_data(self):
        r = self._html

        nodes = [{
            "id": n.name,
            "group": 1,
            "color": n.color or "black",
            "forceX": 1,
            "tooltip": n.tooltip
        } for n in self._nodes]

        links = [{
            "source": l.source,
            "target": l.target,
            "color": l.color,
            "fill": l.fill
        } for l in self._links]

        nodes_json = json.dumps(nodes)
        links_json = json.dumps(links)

        r = (r
             .replace("$data_nodes", nodes_json)
             .replace("$data_links", links_json))
        return r

    def _repr_html_(self):
        return self._render_data()

    def save(self, path: str):
        with open(path, "w") as writer:
            writer.write(self._repr_html_())
