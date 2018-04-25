
from graph import Graph
import pandas as pd

from entities import Shuttle, VelocityModel


class StateGenerator:
    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = StateGenerator()
        return cls.instance

    def __init__(self, start_time='2018-02-14 15:40:00', end_time='2018-02-14 16:05:00'):
        self.time = 0
        self.shuttle = Shuttle(Graph.load_default(), 0, VelocityModel())

    def next_coordinate(self):
        self.time += 1
        self.shuttle.move(self.time)
        position = self.shuttle.current_position()
        return position.y, position.x