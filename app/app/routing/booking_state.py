from functools import reduce


class BookingState:
    """
    Keep track of all bookings. Get's called at each station and
    removes bookings that have been serviced.
    """
    def __init__(self, vehicle_position, bookings=None):
        self.vehicle_position = vehicle_position
        self.bookings_loaded = []
        self.bookings_unloaded = [] if bookings is None else bookings
        self._load_if_possible()

    @property
    def bookings(self):
        return self.bookings_loaded + self.bookings_unloaded

    def add_booking(self, booking):
        self.bookings_unloaded.append(booking)

    def update_vehicle(self, station):
        self.vehicle_position = station
        self._unload_if_possible()
        self._load_if_possible()
        self._update_loaded()

    def passenger_count(self):
        return len(self.bookings_loaded)

    def _load_if_possible(self):
        remove_list = []
        for booking in self.bookings_unloaded:
            if booking.start_node == self.vehicle_position:
                self.bookings_loaded.append(booking)
                remove_list.append(booking)

        for item in remove_list:
            self.bookings_unloaded.remove(item)

    def _unload_if_possible(self):
        for booking in self.bookings_loaded:
            if booking.end_node == self.vehicle_position:
                self.bookings_loaded.remove(booking)

    def _update_loaded(self):
        for booking in self.bookings_loaded:
            booking.start_node = self.vehicle_position
            booking.earliest_departure = 0
            booking.latest_arrival = 10000000  # large number

    def to_geojson(self):
        return self.to_geojson_unloaded() + self.to_geojson_loaded()

    def to_geojson_loaded(self):
        if len(self.bookings_loaded) < 1:
            return []
        return self.flatten([booking.to_geojson_loaded() for booking in self.bookings_loaded])

    def to_geojson_unloaded(self):
        if len(self.bookings_unloaded) < 1:
            return []
        return self.flatten([booking.to_geojson_unloaded() for booking in self.bookings_unloaded])

    @staticmethod
    def flatten(list_of_lists):
        return reduce(list.__add__, list_of_lists)
