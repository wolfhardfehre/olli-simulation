import unittest
import vcr
import pandas as pd
from shapely.geometry import Point
from app.app.routing.schedule import Schedule
from app.app.routing.booking import Booking
from app.app.routing.graph import Graph
from app.app.routing.node import Node

my_vcr = vcr.VCR(
    serializer='yaml',
    cassette_library_dir='tests/fixtures/vcr_cassettes',
    record_mode='once',
    match_on=['uri', 'method'],
)
first = Node(627042770, Point(13.4, 52.3))
second = Node(27785378, Point(13.4, 52.4))
third = Node(2493824077, Point(13.3, 52.4))

booking1 = Booking(first, second, 0, 1800)
booking2 = Booking(second, third, 500, 1800)

node_data = [[627042770, 52.3, 13.4], [27785378, 52.4, 13.4], [2493824077, 52.4, 13.3]]
edge_data = [[627042770, 27785378, 100], [27785378, 2493824077, 550]]
nodes = pd.DataFrame(node_data, columns=['id', 'lat', 'lon'])
nodes.set_index('id', inplace=True)
edges = pd.DataFrame(edge_data, columns=['node1', 'node2', 'distance'])
graph = Graph(nodes, edges)


class ScheduleTest(unittest.TestCase):
    @my_vcr.use_cassette('tests/fixtures/vcr_cassettes/schedule.yaml')
    def test_schedule_stations(self):
        schedule = Schedule([booking1, booking2], first, 'da305144-feeb-4b8d-b843-193be386ff0b', graph=graph)
        self.assertEqual(schedule.station_ids, [627042770, 27785378, 2493824077])

    @my_vcr.use_cassette('tests/fixtures/vcr_cassettes/schedule.yaml')
    def test_schedule_arrival_times(self):
        schedule = Schedule([booking1, booking2], first, 'da305144-feeb-4b8d-b843-193be386ff0b', graph=graph)
        self.assertEqual(schedule.arrival_at(27785378), 650)


if __name__ == '__main__':
    unittest.main()
