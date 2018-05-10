from datetime import datetime
from pytz import timezone, utc
from app.app.entities.moving_entity import MovingEntity
from app.app.entities.tour import Tour

LATITUDE_APPROX = 111320.0
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S%z'


class Shuttle(MovingEntity):

    def __init__(self, graph, time, velocity, battery):
        super().__init__(graph, time)
        self.tour = Tour(graph, velocity, battery)
        self.vehicle_id = "EZ10_G2-005"
        self.velocity = velocity
        self.battery = battery
        self.distance_in_meters = 0.0
        self.edge = None
        self.position = None

    def to_geojson(self):
        position = self.tour.position
        return {
            "geometry": {
                "type": "Point",
                "coordinates": [
                    position.x, position.y
                ]
            },
            "type": "Feature",
            "properties": self._properties()
        }

    def get_route(self):
        return self.tour.to_geojson()

    def _properties(self):
        now = datetime.utcnow()
        local_tz = timezone('Europe/Berlin')
        utc_now = utc.localize(now)
        german = utc_now.astimezone(local_tz)
        return {
            'vehicle_id': self.vehicle_id,
            'last_seen': german.strftime(DATETIME_FORMAT),
            'created_at': now.strftime(DATETIME_FORMAT),
            'theta': '{:.4f} rad'.format(self.tour.azimuth),
            'speed': '{:.2f} m/s'.format(self.tour.speed),
            'battery': '{:.2f} %'.format(self.tour.battery_status),
            'distance': '{:.0f} m'.format(self.tour.total_distance),
            'doors': self.tour.door_status
        }

    def move(self, current_time):
        self.tour.update(current_time)
