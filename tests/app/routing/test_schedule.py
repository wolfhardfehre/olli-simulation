import unittest
import vcr

from app.app.routing.schedule import Schedule
from app.app.routing.booking import Booking

my_vcr = vcr.VCR(
    serializer='yaml',
    cassette_library_dir='tests/fixtures/vcr_cassettes',
    record_mode='once',
    match_on=['uri', 'method'],
)

booking1 = Booking(627042770, 27785378, 0, 1800)
booking2 = Booking(27785378, 2493824077, 500, 1800)

class ScheduleTest(unittest.TestCase):
    @my_vcr.use_cassette('tests/fixtures/vcr_cassettes/schedule.yaml')
    def test_schedule_stations(self):
        schedule = Schedule([booking1, booking2], 627042770, '3c8d0f02-49ce-4c79-92e2-6eb1965205dc')
        self.assertEqual(schedule.station_ids, [627042770, 27785378, 2493824077])

    @my_vcr.use_cassette('tests/fixtures/vcr_cassettes/schedule.yaml')
    def test_schedule_arrival_times(self):
        schedule = Schedule([booking1, booking2], 627042770, '3c8d0f02-49ce-4c79-92e2-6eb1965205dc')
        self.assertEqual(schedule.arrival_at(27785378), 650)

if __name__ == '__main__':
    unittest.main()
