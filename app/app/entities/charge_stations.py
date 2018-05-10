from operator import attrgetter
import pandas as pd
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from app.app.entities.charge_station import ChargeStation
from app.app.routing.dijkstra import shortest_path
from app.app.entities.route import Route


class ChargeStations:

    def __init__(self, tour, graph, velocity, battery):
        self.tour = tour
        self.graph = graph
        self.velocity = velocity
        self.battery = battery
        self.stations = self.__chargers()
        self.target_station = None

    def to_geojson(self):
        return [c.to_geojson() for c in self.stations]

    def get_target_station(self):
        copy = self.target_station
        self.target_station = None
        return copy

    def get_route_to_closest(self, origin_id):
        paths = [shortest_path(self.graph.graph, origin_id, d.node_id) for d in self.stations]
        routes = [Route(self.graph.graph, path, self.tour, self.velocity) for path in paths]
        route = min(routes, key=attrgetter('length'))
        self.target_station = self.stations[routes.index(route)]
        return route

    def __chargers(self):
        df = pd.read_pickle('./resources/charge_stations.p')
        stations = [ChargeStation(row, self.battery) for idx, row in df.iterrows()]
        return [self.__closest(station) for station in stations]

    def __closest(self, station):
        closest = self.graph.get_closest(station.point)
        geom = closest.iloc[0].geometry
        station.lon = geom.x
        station.lat = geom.y
        station.node_id = closest.index.values[0]
        return station
