import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from app.app.routing.dijkstra import shortest_path
from app.app.entities.shuttle import Shuttle
from app.app.routing.graph import Graph
from app.app.entities.models.battery_model import BatteryModel
from app.app.entities.models.velocity_model import VelocityModel
from app.app.routing.booking_state import BookingState
from app.app.routing.schedule import Schedule
from app.app.secret import GRAPHHOPPER_KEY
from datetime import datetime
from pytz import timezone, utc
import time

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S%z'

class FreeFloatShuttle(Shuttle):
    STOP_LIMIT = 40

    def __init__(self, graph, time, velocity_model, battery_model, bookings):
        super().__init__(graph, time, velocity_model, battery_model)
        current_station = 2493824077
        self.graph = graph
        self.node = self.graph.graph[current_station]
        self.booking_state = BookingState(self.node, bookings)
        self.edge_count = 0
        self.position = self.node.geometry
        self.tour = self.__build_tour()
        self.route = self.tour.pop(0)
        self.stopping_at_station_count = 60

    def first_move(self):
        self.pick_next()

    def pick_next(self):
        if self.stopping_at_station_count < self.STOP_LIMIT:
            self.stopping_at_station_count += 1
            self.meters_per_second = 0
            self.position = self.edge.destination.geometry
            return
        print("remaining tours: {0}".format(len(self.tour)))
        if self.edge_count >= len(self.route.edges):
            # try next route
            if len(self.tour) < 1:
                self.position = self.edge.destination.geometry
                self.booking_state.update_vehicle(self.edge.destination)
                print(self.booking_state.passenger_count())
                return
            else:
                self._stop_at_station()
                self.route = self.tour.pop(0)
                self.edge_count = 0

        self.edge = self.route.edges[self.edge_count]
        self.edge_count += 1
        self.position = self.edge.origin.geometry

        self.booking_state.update_vehicle(self.edge.origin)

    def add_booking(self, booking):
        self.booking_state.add_booking(booking)
        self.tour = self.__build_tour()
        self.route = self.tour.pop(0)
        self.edge_count = 0

    def get_route(self):
        return self.route.to_geojson()

    def _stop_at_station(self):
        self.stopping_at_station_count = 0

    def __build_tour(self):
        schedule = Schedule(self.booking_state.bookings, self.booking_state.vehicle_position, GRAPHHOPPER_KEY, self.graph)
        station_list = schedule.station_ids
        assert station_list[0] == self.booking_state.vehicle_position.node_id
        return [shortest_path(self.graph.graph, s, t) for s, t in zip(station_list, station_list[1:])]

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
            'distance': '{:.0f} m'.format(self.distance_in_meters),
            'passenger_count': self.booking_state.passenger_count()
        }
        return self.position, properties

if __name__ == "__main__":
    shuttle = FreeFloatShuttle(Graph.load_default(), 0, VelocityModel(), BatteryModel(), [])
    print(shuttle.to_geojson())
    for t in range(0, 1000):
        shuttle.move(1)
        print(shuttle.to_geojson())
