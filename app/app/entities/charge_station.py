import pandas as pd
from shapely.geometry import Point
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from app.app.entities.story import Story
from app.app.entities.map_point import MapPoint
from app.app.entities.models.battery_model import BatteryModel


class ChargeStation(Story, MapPoint):

    def __init__(self, row, battery, load_capacity=0.5):
        super().__init__(row['lat'], row['lon'])
        self.battery = battery
        self.load_capacity = load_capacity
        self.id = row['id']
        self.name = row['name']
        self.data_type = row['data_type']
        self.node_id = None
        self.start_time = 0
        self.__has_ended = False

    def get_type(self):
        return 'ChargeStation'

    def has_ended(self):
        if self.__has_ended:
            self.__has_ended = False
            self.start_time = 0
            return True
        return False

    def update(self, time):
        if self.start_time == 0:
            self.start_time = time
            return

        delta_time = time - self.start_time
        self.battery.status += delta_time * self.load_capacity

        if self.battery.status >= 100.0:
            self.battery.status = 100.0
            self.__has_ended = True

    @property
    def point(self):
        return Point(self.lon, self.lat)

    def _style(self):
        return {
            "color": "#FCCF40",
            "fillOpacity": 0.5,
            "weight": 2,
            "radius": 20,
            "opacity": 0.7
        }

    def _properties(self):
        return {
            "id": self.id,
            "name": self.name,
            "data_type": self.data_type
        }

    def __repr__(self):
        return 'ChargeStation[id={}, name={}, lat={:.6f}, lon={:.6f}]'.format(
            self.id, self.name, self.lat, self.lon)


if __name__ == '__main__':
    df = pd.read_pickle('./resources/charge_stations.p')
    stations = [ChargeStation(row, BatteryModel()) for idx, row in df.iterrows()]
    [print(station) for station in stations]
