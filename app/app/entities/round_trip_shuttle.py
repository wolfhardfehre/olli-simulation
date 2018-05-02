import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from app.app.routing.dijkstra import shortest_path
from app.app.entities.shuttle import Shuttle
from app.app.routing.graph import Graph
from app.app.entities.models.battery_model import BatteryModel
from app.app.entities.models.velocity_model import VelocityModel


class RoundTripShuttle(Shuttle):

    def __init__(self, graph, time, velocity_model, battery_model, background):
        super().__init__(graph, time, velocity_model, battery_model)
        self.route_count = 0
        self.edge_count = 0
        self.tour = self.__build_tour(background)
        self.route = self.tour[self.route_count]

    def first_move(self):
        self.pick_next()

    def pick_next(self):
        self.route = self.tour[self.route_count]
        self.edge = self.route.edges[self.edge_count]
        self.position = self.edge.origin.geometry
        self.edge_count += 1
        if self.edge_count >= len(self.route.edges):
            self.route_count += 1
            self.edge_count = 0
            if self.route_count >= len(self.tour):
                self.route_count = 0

    def get_route(self):
        return self.route.to_geojson()

    def __build_tour(self, background):
        station_ids = background.closest_station_ids
        station_ids = station_ids + [station_ids[0]]
        return [shortest_path(self.graph, o, d) for o, d in zip(station_ids[:-1], station_ids[1:])]


if __name__ == "__main__":
    shuttle = RoundTripShuttle(Graph.load_default(), 0, VelocityModel(), BatteryModel())
    print(shuttle.to_geojson())
    for t in range(0, 1000):
        shuttle.move(1)
        print(shuttle.to_geojson())
