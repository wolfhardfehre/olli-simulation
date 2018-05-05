import unittest
from app.app.routing.booking_state import BookingState
from app.app.routing.booking import Booking


class ScheduleTest(unittest.TestCase):
    def test_add_booking(self):
        bookings = [Booking(1, 2, 0, 100), Booking(2, 3, 0, 100)]
        booking_state = BookingState(1)
        booking_state.add_booking(bookings[0])
        booking_state.add_booking(bookings[1])

        self.assertEqual(booking_state.bookings, bookings)

    def test_booking_gets_removed_when_served(self):
        bookings = [Booking(1, 2, 0, 1), Booking(1, 3, 0, 100), Booking(3, 4, 0, 100)]
        booking_state = BookingState(1, bookings)
        self.assertEqual(len(booking_state.bookings_loaded), 2)
        booking_state.update_vehicle(2)
        self.assertEqual(len(booking_state.bookings_loaded), 1)
        booking_state.update_vehicle(3)
        self.assertEqual(len(booking_state.bookings_loaded), 1)
        booking_state.update_vehicle(4)
        self.assertEqual(len(booking_state.bookings_loaded), 0)

    def test_bookings_updates_start(self):
        bookings = [Booking(1, 3, 0, 1)]
        booking_state = BookingState(1, bookings)
        booking_state.update_vehicle(2)
        self.assertEqual(booking_state.bookings[0].start_node, 2)


if __name__ == '__main__':
    unittest.main()
