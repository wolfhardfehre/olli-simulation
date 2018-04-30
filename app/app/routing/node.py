class Node:
    def __init__(self, node_id, geometry):
        self.node_id = node_id
        self.geometry = geometry
        self.neighbors = {}

    def add_neighbor(self, node_id, distance):
        self.neighbors[node_id] = distance

    def __repr__(self):
        return 'Node[id={}, geom={}, neighbors={}]'.format(
            self.node_id, self.geometry, self.neighbors)
