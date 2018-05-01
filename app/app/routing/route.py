import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from app.app.routing.edge import Edge


class Route:

    def __init__(self, graph, path):
        self.nodes = [graph[node_id] for node_id in path]
        self.edges = self.__edges()
        self.__length = None
        self.__geojson = None

    def __edges(self):
        return [self.to_edge(o, d) for o, d in self.__zip_nodes()]

    def __zip_nodes(self):
        return zip(self.nodes[:-1], self.nodes[1:])

    @staticmethod
    def to_edge(origin, destination):
        return Edge(origin, destination)

    def length(self):
        if self.__length is None:
            self.__length = sum(edge.distance for edge in self.edges)
        return self.__length

    def to_geojson(self):
        if self.__geojson is None:
            return {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[node.geometry.x, node.geometry.y] for node in self.nodes]
                },
                "style": {
                    "color": "#3182BD",
                    "weight": 5,
                    "opacity": 0.7
                },
                "properties": {
                    "length": self.length(),
                    "id": '000'
                }
            }
        return self.__geojson

    def __repr__(self):
        return 'Route[length={:.0f}m, origin={}, destination={}]'.format(self.length(), self.nodes[0], self.nodes[-1])
