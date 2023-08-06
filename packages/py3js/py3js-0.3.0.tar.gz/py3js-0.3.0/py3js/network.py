from importlib import resources
import json
from typing import List
import base64


class Node:
    def __init__(self, name: str, tooltip: str = None, color: str = None, level: int = None,
                 radius: int = 8,
                 stroke_color: str = "black",
                 stroke_width: int = 1):
        self.name = name
        self.tooltip = tooltip or name
        self.color = color
        self.level = level
        self.radius = radius
        self.stroke_color = stroke_color
        self.stroke_width = stroke_width


class Link:
    def __init__(self, source: str, target: str, color: str = "black", fill: str = "black",
                 opacity: float = 0.5,
                 width: float = 1,
                 is_arrow: bool = True):
        self.source = source
        self.target = target
        self.color = color
        self.fill = fill
        self.opacity = opacity
        self.width = width
        self.is_arrow = is_arrow


class ForceDirectedGraph:

    def __init__(self, width: int = 800, height: int = 600, x_levels: int = -1,
                 collision_radius: int = 8,
                 show_node_names: bool = False,
                 arrow_radius: int = 8):
        self._html = resources.read_text("py3js", "force.html")
        self._html = (self._html
                      .replace("$width", str(width))
                      .replace("$height", str(height))
                      .replace("$x_levels", str(x_levels))
                      .replace("$collision_radius", str(collision_radius))
                      .replace("$showNodeNames", "true" if show_node_names else "false")
                      .replace("$arrowRadius", str(arrow_radius)))
        self._width = width
        self._height = height

        self._nodes: List[Node] = []
        self._links: List[Link] = []

    def add_nodes(self, *node: Node):
        for n in node:
            self._nodes.append(n)

    def add_links(self, *link: Link):
        for l in link:
            self._links.append(l)

    def _render_data(self):
        r = self._html

        nodes = [{
            "id": n.name,
            "color": n.color or "black",
            "level": n.level,
            "tooltip": n.tooltip,
            "radius": n.radius,
            "stroke": n.stroke_color,
            "stroke_width": n.stroke_width
        } for n in self._nodes]

        links = [{
            "source": l.source,
            "target": l.target,
            "color": l.color,
            "fill": l.fill,
            "opacity": l.opacity,
            "width": l.width,
            "arrow": l.is_arrow
        } for l in self._links]

        nodes_json = json.dumps(nodes)
        links_json = json.dumps(links)

        r = (r
             .replace("$data_nodes", nodes_json)
             .replace("$data_links", links_json))
        return r

    def _repr_html_(self):
        data = self._render_data()
        b64data = base64.b64encode(data.encode("utf-8")).decode("utf-8")
        url = f"data:text/html;charset=utf-8;base64,{b64data}"
        return f"<iframe src=\"{url}\" width=\"{self._width}\" height=\"{self._height}\" scrolling=\"no\" style=\"border:none !important;\"></iframe>"



    def save(self, path: str):
        with open(path, "w") as writer:
            writer.write(self._repr_html_())
