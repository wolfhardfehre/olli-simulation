from shapely.geometry import Point
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from app.app.entities.story import Story
from app.app.entities.map_point import MapPoint


class TransportStation(Story, MapPoint):

    def __init__(self, row, tour, wait_time=20):
        super().__init__(row['lat'], row['lon'])
        self.id = row['id']
        self.type = row['type']
        self.name = row['name']
        self.products = row['products']
        self.tour = tour
        self.wait_time = wait_time
        self.node_id = None
        self.start_time = 0
        self.__has_ended = False

    def get_type(self):
        return 'TransportStation'

    def has_ended(self):
        if self.__has_ended:
            self.__has_ended = False
            self.start_time = 0
            return True
        return False

    def update(self, time):
        self.__update_tour()
        if self.start_time == 0:
            self.start_time = time
        elif time - self.start_time > self.wait_time:
            self.__has_ended = True
        else:
            self.__has_ended = False

    @property
    def point(self):
        return Point(self.lon, self.lat)

    def _style(self):
        return {
            "color": "#9966CC",
            "fillOpacity": 0.5,
            "weight": 2,
            "radius": 30,
            "opacity": 0.7
        }

    def _properties(self):
        return {
            "id": self.id,
            "type": self.type,
            "name": self.name,
            "products": self.products
        }

    def __update_tour(self):
        self.tour.change_speed(0)
        self.tour.change_doors('open')
        self.tour.change_meters(0)
        self.tour.change_position(Point(self.lon, self.lat))

    def __repr__(self):
        return 'TransportStation[id={}, name={}, lat={:.6f}, lon={:.6f}]'.format(
            self.id, self.name, self.lat, self.lon)
