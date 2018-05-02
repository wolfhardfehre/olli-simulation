import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from app.app.entities.shuttle import Shuttle
from app.app.routing.graph import Graph
from app.app.entities.models.battery_model import BatteryModel
from app.app.entities.models.velocity_model import VelocityModel
from app.app.entities.tour import Tour


class RoundTripShuttle(Shuttle):

    def __init__(self, graph, time, velocity_model, battery_model, background):
        super().__init__(graph, time, velocity_model, battery_model)
        self.tour = Tour(graph, background)

    def first_move(self):
        self.pick_next()

    def pick_next(self):
        self.position, self.edge = self.tour.next_story()

    def get_route(self):
        return self.tour.get_route()


if __name__ == "__main__":
    shuttle = RoundTripShuttle(Graph.load_default(), 0, VelocityModel(), BatteryModel())
    print(shuttle.to_geojson())
    for t in range(0, 1000):
        shuttle.move(1)
        print(shuttle.to_geojson())
