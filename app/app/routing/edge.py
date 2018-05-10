import math
from shapely.geometry import Polygon


class Edge:
    """
    Edge of a graph consisting of two
    nodes and the distance between them.
    """
    EPSILON = 0.000001

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

    @property
    def azimuth(self):
        if self.__azimuth is None:
            start = self.origin.geometry
            end = self.destination.geometry
            self.__azimuth = math.atan2(end.y - start.y, end.x - start.x)
        return self.__azimuth

    @property
    def bounding_box(self):
        if self.__bbox is None:
            start = self.origin.geometry
            end = self.destination.geometry
            min_x = min(start.x, end.x) - Edge.EPSILON
            max_x = max(start.x, end.x) + Edge.EPSILON
            min_y = min(start.y, end.y) - Edge.EPSILON
            max_y = max(start.y, end.y) + Edge.EPSILON
            self.__bbox = Polygon((
                (max_x, max_y),
                (max_x, min_y),
                (min_x, min_y),
                (min_x, max_y)
            ))
        return self.__bbox