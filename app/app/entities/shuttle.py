import abc
import math
from datetime import datetime
from pytz import timezone, utc
from shapely.geometry import Point
from app.app.entities.entity import Entity


LATITUDE_APPROX = 111320.0
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S%z'


class Shuttle(Entity):
    __metaclass__ = abc.ABCMeta

    def __init__(self, graph, time, velocity_model, battery_model):
        super().__init__(graph, time)
        self.vehicle_id = "EZ10_G2-005"
        self.velocity_model = velocity_model
        self.battery_model = battery_model
        self.degrees_per_hour = 0.0
        self.edge = None
        self.position = None
        self.first_move()

    @abc.abstractmethod
    def first_move(self):
        NotImplementedError()

    @abc.abstractmethod
    def pick_next(self):
        NotImplementedError()

    def current_state(self):
        now = datetime.utcnow()
        local_tz = timezone('Europe/Berlin')
        utc_now = utc.localize(now)
        german = utc_now.astimezone(local_tz)
        properties = {
            'vehicle_id': self.vehicle_id,
            'theta': '{:.4f}'.format(self.edge.azimuth()),
            'speed': self.degrees_per_hour * LATITUDE_APPROX,
            'last_seen': german.strftime(DATETIME_FORMAT),
            'created_at': now.strftime(DATETIME_FORMAT),
            'battery': self.battery_model.current_status()
        }
        return self.position, properties

    def move(self, current_time):
        self.degrees_per_hour = self.velocity_model.current_velocity()
        delta_degrees = self.degrees_per_hour * (current_time - self.time)
        x = self.position.x + delta_degrees * math.cos(self.edge.azimuth())
        y = self.position.y + delta_degrees * math.sin(self.edge.azimuth())
        self.position = Point((x, y))
        if not self.position.within(self.edge.bounding_box()):
            self.pick_next()
        self.time = current_time
