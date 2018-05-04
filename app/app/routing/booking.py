class Booking:
    counter = 1000

    @classmethod
    def get_counter(cls):
        cls.counter += 1
        return cls.counter

    # unix times, graph ids
    def __init__(self, start_station, end_station, earliest_departure, latest_arrival):
        self.start_station = start_station
        self.end_station = end_station
        self.earliest_departure = earliest_departure
        self.latest_arrival = latest_arrival

    def to_geojson_unloaded(self):
        return [self.geojson_point(p, Booking.get_counter(), color) for p, color in [(self.start_station.geometry,'#9DBD0F'), (self.end_station.geometry,'#3110BD')]]

    def to_geojson_loaded(self):
        return [self.geojson_point(self.end_station.geometry, Booking.get_counter())]

    def geojson_point(self, point, id, color='#3110BD'):
        return {
            "geometry": {
                "type": "Point",
                "coordinates": [
                    point.x, point.y
                ]
            },
            "type": "Feature",
            "style": {
                "color": color,
                "fillOpacity": 0.5,
                "weight": 2,
                "radius": 20,
                "opacity": 0.7
            },
            "properties": {
                "id": id
            }
        }