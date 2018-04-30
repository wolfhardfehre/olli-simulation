import math
from shapely.geometry import Polygon


class Edge:
    """
    Edge of a graph consisting of two
    nodes and the distance between them.
    """
    def __init__(self, origin, destination):
        """
        Parameters
        ----------
        origin: Node
            start node of an edge
        destination: Node
            end node of an edge
        """
        self.origin = origin
        self.destination = destination
        self.distance = origin.neighbors[destination.node_id]
        self.__azimuth = None
        self.__bbox = None

    def azimuth(self):
        if self.__azimuth is None:
            start = self.origin.geometry
            end = self.destination.geometry
            self.__azimuth = math.atan2(end.y - start.y, end.x - start.x)
        return self.__azimuth

    def bounding_box(self):
        if self.__bbox is None:
            start = self.origin.geometry
            end = self.destination.geometry
            self.__bbox = Polygon(((start.x, start.y), (start.x, end.y), (end.x, end.y), (end.x, start.y)))
        return self.__bbox