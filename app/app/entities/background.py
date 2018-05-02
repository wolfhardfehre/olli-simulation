import pandas as pd
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from app.app.entities.entity import Entity
from app.app.entities.charge_station import ChargeStation
from app.app.entities.transport_station import TransportStation
from app.app.routing.graph import Graph


class Background(Entity):

    def __init__(self, graph):
        self.graph = graph
        self.charge_station = self.__chargers()
        self.transport_stations = self.__public_transport()

    @property
    def closest_station_ids(self):
        return [self.__closest(station) for station in self.transport_stations]

    def __closest(self, station):
        closest = self.graph.get_closest(station.point)
        geom = closest.iloc[0].geometry
        station.lon = geom.x
        station.lat = geom.y
        return closest.index.values[0]

    def to_geojson(self):
        return [c.to_geojson() for c in self.charge_station] + \
               [t.to_geojson() for t in self.transport_stations]

    @staticmethod
    def __chargers():
        df = pd.read_pickle('./resources/charge_stations.p')
        return [ChargeStation(row) for idx, row in df.iterrows()]

    @staticmethod
    def __public_transport():
        df = pd.read_pickle('./resources/public_transport.p')
        return [TransportStation(row) for idx, row in df.iterrows()]


if __name__ == '__main__':
    background = Background(Graph.load_default())
    print(background.closest_station_ids)
