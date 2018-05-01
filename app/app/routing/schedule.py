from app.app.routing.graphhopper import Graphhopper
# Build a schedule
class Schedule:
    def __init__(self, booking_list, start_position):
        self.booking_list = booking_list
        self.start_position = start_position
        self.id = 0
        # compute new schedule
        g = Graphhopper()
        job_id = g.post_problem(self._query())
        self.solution = g.get_solution(job_id)

    @property
    def station_ids(self):
        return [activity.get('location_id') for activity in self.solution.get('routes')[0].get('activities')]

    def arrival_for(self, station_id):
        return 0

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
            "shipments": self._shipments
        }

    @property
    def _vehicles(self):
        return {
            "vehicle_id": "olli",
            "type_id": "eshuttle",
            "start_address": {
                "location_id": str(self.start_position),
                "lon": self._stations[self.start_position]['longitude'],
                "lat": self._stations[self.start_position]['latitude']
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
                        "lon": self._stations.get(booking.start_station).get('longitude'),
                        "lat": self._stations.get(booking.start_station).get('latitude')
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
                        "lon": self._stations.get(booking.end_station).get('longitude'),
                        "lat": self._stations.get(booking.end_station).get('latitude')
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
    def _stations(self):
        return {
            627042770: {
                "longitude": 13.3568719,
                "latitude": 52.4815767
            },
            27785378: {
                "longitude": 13.3587658,
                "latitude": 52.4857809
            },
            2493824077: {
                "longitude": 13.3498653,
                "latitude": 52.4794034
            }
        }

    def next_id(self):
        self.id += 1
        return str(self.id)