import pandas as pd
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from app.app.routing.dijkstra import shortest_path
from app.app.entities.shuttle import Shuttle
from app.app.routing.graph import Graph
from app.app.entities.models.battery_model import BatteryModel
from app.app.entities.models.velocity_model import VelocityModel


class RoundTripShuttle(Shuttle):

    def first_move(self):
        self.tour = self.__build_tour()
        self.route_count = 0
        self.edge_count = 0
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

    def get_ground_data(self):
        return self.stations + [self.__build_route(self.route)]

    def __build_tour(self):
        stations = pd.read_csv("./resources/stations.csv", delimiter=";")
        self.stations = self.__build_stations(stations)
        station_ids = stations["id"].tolist()
        station_ids = station_ids + [station_ids[0]]
        return [shortest_path(self.graph, o, d) for o, d in zip(station_ids[:-1], station_ids[1:])]

    def __build_stations(self, stations):
        return [self.__build_station_geojson(row) for index, row in stations.iterrows()]

    @staticmethod
    def __build_station_geojson(station_row):
        return {
            "geometry": {
                "type": "Point",
                "coordinates": [
                    station_row["lng"], station_row["lat"]
                ]
            },
            "type": "Feature",
            "style": {
                "color": "#9966CC",
                "fillOpacity": 0.5,
                "weight": 2,
                "radius": 30,
                "opacity": 0.7
            },
            "properties": {
                "id": station_row['id']
            }
        }

    @staticmethod
    def __build_route(route):
        return route.to_geojson()


if __name__ == "__main__":
    shuttle = RoundTripShuttle(Graph.load_default(), 0, VelocityModel(), BatteryModel())
    print(shuttle.current_state())
    for t in range(0, 1000):
        shuttle.move(1)
        print(shuttle.current_state())
