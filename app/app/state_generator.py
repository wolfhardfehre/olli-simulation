from graph import Graph
from entities import Shuttle, VelocityModel


class StateGenerator:
    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = StateGenerator()
        return cls.instance

    def __init__(self):
        self.time = 0.0
        self.shuttle = Shuttle(Graph.load_default(), self.time, VelocityModel())

    def next_coordinate(self):
        self.time += 1
        self.shuttle.move(self.time)
        position = self.shuttle.current_position()
        return position.y, position.x