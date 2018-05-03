import sys
import time

# Keep track of all bookings. Get's called at each station and removes bookings that have been serviced
class BookingState:
    def __init__(self, vehicle_position, bookings=[]):
        self.vehicle_position = vehicle_position
        self.bookings_loaded = []
        self.bookings_unloaded = bookings
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
        stopped = False
        for booking in self.bookings_unloaded:
            if booking.start_station == self.vehicle_position:
                self.bookings_loaded.append(booking)
                self.bookings_unloaded.remove(booking)
                stopped = True

        if stopped:
            time.sleep(1)

    def _unload_if_possible(self):
        stopped = False
        for booking in self.bookings_loaded:
            if booking.end_station == self.vehicle_position:
                self.bookings_loaded.remove(booking)
                stopped = True
        if stopped:
            time.sleep(1)

    def _update_loaded(self):
        for booking in self.bookings_loaded:
            booking.start_station = self.vehicle_position
            booking.earliest_departure = 0
            booking.latest_arrival = sys.maxsize