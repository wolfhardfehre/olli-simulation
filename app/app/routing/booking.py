class Booking:
    counter = 1000

    @classmethod
    def get_counter(cls):
        cls.counter += 1
        return cls.counter

    def __init__(self, start_node, end_node, earliest_departure, latest_arrival):
        self.start_node = start_node
        self.end_node = end_node
        self.earliest_departure = earliest_departure
        self.latest_arrival = latest_arrival

    def to_geojson_unloaded(self):
        return [self.geojson_point(p, Booking.get_counter(), color) for p, color in
                [(self.start_node.geometry, '#9DBD0F'), (self.end_node.geometry, '#3110BD')]]

    def to_geojson_loaded(self):
        return [self.geojson_point(self.end_node.geometry, Booking.get_counter())]

    @staticmethod
    def geojson_point(point, id, color='#3110BD'):
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
