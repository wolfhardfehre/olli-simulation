from app.app.routing.graph import Graph
from app.app.entities.entities import Shuttle, VelocityModel, BatteryModel


class StateGenerator:
    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = StateGenerator()
        return cls.instance

    def __init__(self):
        self.time = 0.0
        self.shuttle = Shuttle(Graph.load_default(), self.time, VelocityModel(), BatteryModel())

    def next(self):
        self.time += 1
        self.shuttle.move(self.time)
        position, properties = self.shuttle.current_state()
        return position.x, position.y, properties