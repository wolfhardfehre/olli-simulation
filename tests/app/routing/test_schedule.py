import unittest
import vcr

from app.app.routing.schedule import Schedule
from app.app.routing.booking import Booking
from app.app.routing.graph import Graph
import pandas as pd

my_vcr = vcr.VCR(
    serializer='yaml',
    cassette_library_dir='tests/fixtures/vcr_cassettes',
    record_mode='once',
    match_on=['uri', 'method'],
)

booking1 = Booking(627042770, 27785378, 0, 1800)
booking2 = Booking(27785378, 2493824077, 500, 1800)

node_data = [[627042770, 52.3, 13.4], [27785378, 52.4, 13.4], [2493824077, 52.4, 13.3]]
edge_data = [[627042770, 27785378, 100], [27785378, 2493824077, 550]]
nodes = pd.DataFrame(node_data, columns=['id', 'lat', 'lon'])
nodes.set_index('id', inplace=True)
edges = pd.DataFrame(edge_data, columns=['node1', 'node2', 'distance'])
graph = Graph(nodes, edges)

class ScheduleTest(unittest.TestCase):
    @my_vcr.use_cassette('tests/fixtures/vcr_cassettes/schedule.yaml')
    def test_schedule_stations(self):
        schedule = Schedule([booking1, booking2], 627042770, 'da305144-feeb-4b8d-b843-193be386ff0b', graph=graph)
        self.assertEqual(schedule.station_ids, [627042770, 27785378, 2493824077])

    @my_vcr.use_cassette('tests/fixtures/vcr_cassettes/schedule.yaml')
    def test_schedule_arrival_times(self):
        schedule = Schedule([booking1, booking2], 627042770, 'da305144-feeb-4b8d-b843-193be386ff0b',graph=graph)
        self.assertEqual(schedule.arrival_at(27785378), 650)

if __name__ == '__main__':
    unittest.main()
