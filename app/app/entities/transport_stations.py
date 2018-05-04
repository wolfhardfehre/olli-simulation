import pandas as pd
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from app.app.entities.transport_station import TransportStation


class TransportStations:

    def __init__(self, tour, graph):
        self.tour = tour
        self.graph = graph
        self.stations = self.__public_transport()
        self.station_count = 1

    def get_next(self):
        station = self.stations[self.station_count]
        self.station_count += 1
        if self.station_count == len(self.stations):
            self.station_count = 0
        return station

    def to_geojson(self):
        return [t.to_geojson() for t in self.stations]

    def __public_transport(self):
        df = pd.read_pickle('./resources/public_transport.p')
        stations = [TransportStation(row, self.tour) for idx, row in df.iterrows()]
        return [self.__closest(station) for station in stations]

    def __closest(self, station):
        closest = self.graph.get_closest(station.point)
        geom = closest.iloc[0].geometry
        station.lon = geom.x
        station.lat = geom.y
        station.node_id = closest.index.values[0]
        return station
