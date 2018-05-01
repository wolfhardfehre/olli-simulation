import random
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from app.app.entities.shuttle import Shuttle
from app.app.routing.graph import Graph
from app.app.entities.models.battery_model import BatteryModel
from app.app.entities.models.velocity_model import VelocityModel
from app.app.routing.edge import Edge


class RandomShuttle(Shuttle):

    def first_move(self):
        self.edge = self.__seed()
        self.position = self.edge.origin.geometry

    def pick_next(self):
        self.edge = self.__next_edge(self.edge)
        self.position = self.edge.origin.geometry

    def __seed(self):
        node_ids = self.__keys(self.graph)
        start_id = self.__random(node_ids)
        start = self.graph[start_id]
        end = self.__seed_end_node(start, None)
        return Edge(start, end)

    def __next_edge(self, previous):
        start = previous.destination
        end = self.__seed_end_node(start, previous.origin.node_id)
        return Edge(start, end)

    def __seed_end_node(self, node, exclude=None):
        neighbors = self.__keys(node.neighbors)
        if exclude is not None and exclude in neighbors and len(neighbors) > 1:
            neighbors.remove(exclude)
        return self.graph[self.__random(neighbors)]

    @staticmethod
    def __keys(some_dict):
        return list(some_dict.keys())

    @staticmethod
    def __random(some_list):
        return random.choice(some_list)


if __name__ == '__main__':
    shuttle = RandomShuttle(Graph.load_default(), 0, VelocityModel(), BatteryModel())
    print(shuttle.current_state())
    for t in range(0, 100):
        shuttle.move(1)
        print(shuttle.current_state())
