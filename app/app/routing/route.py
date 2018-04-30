from shapely.geometry import LineString

# A route describes the way from a node A to a node B
class Route:
    def __init__(self, vertex_list):
        self.vertex_list = vertex_list

    @property
    def geometry(self):
        return LineString([v.geometry for v in self.vertex_list])