import sys

# Keep track of all bookings. Get's called at each station and removes bookings that have been serviced
class BookingState:
    def __init__(self, vehicle_position, bookings=[]):
        self.vehicle_position = vehicle_position
        self.bookings = bookings
        self.bookings_loaded = []
        self.bookings_not_loaded = []
        self._load_if_possible()

    def add_booking(self, booking):
        self.bookings.append(booking)

    def update_vehicle(self, station):
        self.vehicle_position = station
        self._unload_if_possible()
        self._load_if_possible()
        self._update_loaded()

    def _load_if_possible(self):
        for booking in self.bookings:
            if booking.start_station == self.vehicle_position:
                self.bookings_loaded.append(booking)

    def _unload_if_possible(self):
        for booking in self.bookings_loaded:
            if booking.end_station == self.vehicle_position:
                self.bookings_loaded.remove(booking)
                self.bookings.remove(booking)

    def _update_loaded(self):
        for booking in self.bookings_loaded:
            booking.start_station = self.vehicle_position
            booking.earliest_departure = 0
            booking.latest_arrival = sys.maxsize