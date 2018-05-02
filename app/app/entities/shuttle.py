import abc
import math
from datetime import datetime
from pytz import timezone, utc
from shapely.geometry import Point
from app.app.entities.moving_entity import MovingEntity


LATITUDE_APPROX = 111320.0
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S%z'


class Shuttle(MovingEntity):
    __metaclass__ = abc.ABCMeta

    def __init__(self, graph, time, velocity_model, battery_model):
        super().__init__(graph, time)
        self.vehicle_id = "EZ10_G2-005"
        self.velocity_model = velocity_model
        self.battery_model = battery_model
        self.meters_per_second = 0.0
        self.distance_in_meters = 0.0
        self.edge = None
        self.position = None

    @abc.abstractmethod
    def first_move(self):
        NotImplementedError()

    @abc.abstractmethod
    def pick_next(self):
        NotImplementedError()

    def to_geojson(self):
        position, properties = self.__current_state()
        return {
            "geometry": {
                "type": "Point",
                "coordinates": [
                    position.x, position.y
                ]
            },
            "type": "Feature",
            "properties": properties
        }

    def __current_state(self):
        now = datetime.utcnow()
        local_tz = timezone('Europe/Berlin')
        utc_now = utc.localize(now)
        german = utc_now.astimezone(local_tz)
        properties = {
            'vehicle_id': self.vehicle_id,
            'theta': '{:.4f} rad'.format(self.edge.azimuth()),
            'speed': '{:.2f} m/s'.format(self.meters_per_second),
            'last_seen': german.strftime(DATETIME_FORMAT),
            'created_at': now.strftime(DATETIME_FORMAT),
            'battery': '{:.2f} %'.format(self.battery_model.current_status()),
            'distance': '{:.0f} m'.format(self.distance_in_meters)
        }
        return self.position, properties

    def move(self, current_time):
        self.meters_per_second = self.velocity_model.current_velocity()
        degrees_per_second = self.meters_per_second / LATITUDE_APPROX
        delta_time = (current_time - self.time)
        delta_degrees = degrees_per_second * delta_time
        delta_meters = self.meters_per_second * delta_time
        self.distance_in_meters += delta_meters
        self.battery_model.update(delta_meters)
        x = self.position.x + delta_degrees * math.cos(self.edge.azimuth())
        y = self.position.y + delta_degrees * math.sin(self.edge.azimuth())
        self.position = Point((x, y))
        if not self.position.within(self.edge.bounding_box()):
            self.pick_next()
        self.time = current_time
        if self.battery_model.low_battery():
            print("should route to next charger")
