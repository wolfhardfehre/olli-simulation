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

class FreeFloatShuttle(Shuttle):

    def __init__(self, graph, time, velocity_model, battery_model, bookings):
        super().__init__(graph, time, velocity_model, battery_model)
        current_station = 2493824077
        self.booking_state = BookingState(current_station, bookings)
        self.graph = graph
        self.edge_count = 0
        self.position = graph.nodes.loc[current_station]
        self.tour = self.__build_tour()
        self.route = self.tour.pop(0)

    def first_move(self):
        self.pick_next()

    def pick_next(self):
        if self.edge_count >= len(self.route.edges):
            # try next route
            if len(self.tour) < 1:
                self.position = self.edge.destination.geometry
                self.booking_state.update_vehicle(self.edge.destination.node_id)
                print(self.booking_state.passenger_count())
                return
            else:
                self.route = self.tour.pop(0)
                self.edge_count = 0

        self.edge = self.route.edges[self.edge_count]
        self.edge_count += 1
        self.position = self.edge.origin.geometry

        self.booking_state.update_vehicle(self.edge.origin.node_id)

    def add_booking(self, booking):
        self.booking_state.add_booking(booking)
        self.tour = self.__build_tour()
        self.route = self.tour.pop(0)
        self.edge_count = 0

    def get_route(self):
        return self.route.to_geojson()

    def __build_tour(self):
        schedule = Schedule(self.booking_state.bookings, self.booking_state.vehicle_position, GRAPHHOPPER_KEY, self.graph)
        station_list = schedule.station_ids
        assert station_list[0] == self.booking_state.vehicle_position
        return [shortest_path(self.graph.graph, s, t) for s, t in zip(station_list, station_list[1:])]

if __name__ == "__main__":
    shuttle = FreeFloatShuttle(Graph.load_default(), 0, VelocityModel(), BatteryModel())
    print(shuttle.to_geojson())
    for t in range(0, 1000):
        shuttle.move(1)
        print(shuttle.to_geojson())
