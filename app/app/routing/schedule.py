from app.app.routing.graphhopper import Graphhopper
from app.app.routing.graph import Graph
from app.app.routing.dijkstra import shortest_path
from functools import reduce

# Build a schedule
class Schedule:
    METERS_PER_SECOND = 2.2

    def __init__(self, booking_list, start_position, api_key, graph = Graph.load_default()):
        self.booking_list = booking_list
        self.start_position = start_position
        self.id = 0
        self.graph = graph
        # compute new schedule
        g = Graphhopper(api_key=api_key)
        job_id = g.post_problem(self._query())
        self.solution = g.get_solution(job_id)

    @property
    def station_ids(self):
        # return uniq locations and map to ints
        locations = [int(activity.get('location_id')) for activity in self._activities]
        return reduce(lambda l, x: l if x in l else l+[x], locations, [])

    def arrival_at(self, station_id):
        for activity in self._activities:
            if activity.get('location_id') == str(station_id):
                return activity.get('arr_time')

    @property
    def _activities(self):
        return self.flatten([route.get('activities') for route in self._routes()])

    def _routes(self):
        return self.solution.get('routes')

    def _query(self):
        return {
            "vehicles": [self._vehicles],
            "vehicle_types": [
                {
                    "type_id": "eshuttle",
                    "profile": "bike",
                    "capacity": [12],
                    "speed_factor": 0.7,
                }
            ],
            "shipments": self._shipments,
            "cost_matrices": [
                {
                    "profile": "eshuttle",
                    "location_ids": self._stops,
                    "data": {
                        "distances": self._distance_matrix(),
                        "times": self._time_matrix()
                    }
                }
            ]
        }

    @property
    def _vehicles(self):
        return {
            "vehicle_id": "olli",
            "type_id": "eshuttle",
            "start_address": {
                "location_id": str(self.start_position),
                "lon": self.graph.nodes.loc[self.start_position].geometry.x,
                "lat": self.graph.nodes.loc[self.start_position].geometry.y,
            },
            "return_to_depot": False
        }

    @property
    def _shipments(self):
        return [
            {
                "id": self.next_id(),
                "pickup": {
                    "address": {
                        "location_id": str(booking.start_station),
                        "lon": self.graph.nodes.loc[booking.start_station].geometry.x,
                        "lat": self.graph.nodes.loc[booking.start_station].geometry.y,
                    },
                    "duration": 60,
                    "time_windows": [
                        {
                            "earliest": booking.earliest_departure,
                            "latest": booking.earliest_departure + 600
                        }
                    ]
                },
                "delivery": {
                    "address": {
                        "location_id": str(booking.end_station),
                        "lon": self.graph.nodes.loc[booking.end_station].geometry.x,
                        "lat": self.graph.nodes.loc[booking.end_station].geometry.y,
                    },
                    "duration": 60,
                    "time_windows": [
                        {
                            "latest": booking.latest_arrival
                        }
                    ]
                },
                "size": [1],
            } for booking in self.booking_list]

    @property
    def _stops(self):
        return [627042770, 27785378, 2493824077]

    def flatten(self, listOfLists):
        return reduce(list.__add__, listOfLists)

    def next_id(self):
        self.id += 1
        return str(self.id)

    def _time_matrix(self):
        return [[y * self.METERS_PER_SECOND for y in x] for x in self._distance_matrix()]

    def _distance_matrix(self):
        return [[shortest_path(self.graph.graph, s, t).length() for t in self._stops] for s in self._stops]