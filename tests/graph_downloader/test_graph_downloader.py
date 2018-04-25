import unittest
import vcr
import requests
import os

print(os.getcwd())

from app.graph_downloader.graph_downloader import QUERY_TEMPLATE
from app.graph_downloader.graph_downloader import Downloader
from app.graph_downloader.graph_downloader import DEFAULT_URL

my_vcr = vcr.VCR(
    serializer='yaml',
    cassette_library_dir='fixtures/vcr_cassettes',
    record_mode='once',
    match_on=['uri', 'method'],
)


NORTH = 52.484421
SOUTH = 52.479951
WEST = 13.352029
EAST = 13.359325
BBOX = [SOUTH, WEST, NORTH, EAST]


class DownloaderTest(unittest.TestCase):

    @my_vcr.use_cassette('fixtures/vcr_cassettes/overpass.yaml')
    def test_downloading_and_graph_building(self):
        params = dict(data=QUERY_TEMPLATE.format(*BBOX))
        response = requests.get(url=DEFAULT_URL, params=params).json()
        downloader = Downloader(response)

        self.assertEqual(443, len(downloader.nodes.index))
        self.assertEqual(489, len(downloader.edges.index))


if __name__ == '__main__':
    unittest.main()
