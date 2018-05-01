import unittest

import vcr

from app.app.routing.graphhopper import Graphhopper

my_vcr = vcr.VCR(
    serializer='yaml',
    cassette_library_dir='tests/fixtures/vcr_cassettes',
    record_mode='once',
    match_on=['uri', 'method'],
)

problem = \
            {
              "vehicles": [
                {
                  "vehicle_id": "my_vehicle",
                  "start_address": {
                    "location_id": "627042770",
                    "lon": 13.3568719,
                    "lat": 52.4815767
                  }
                }
              ],
              "services": [
                {
                  "id": "jlb",
                  "address": {
                    "location_id": "27785378",
                    "lon": 13.3587658,
                    "lat": 52.4857809
                  }
                }
              ]
            }

graphhopper = Graphhopper()


class GraphhopperTest(unittest.TestCase):
    @my_vcr.use_cassette('tests/fixtures/vcr_cassettes/graphhopper.yaml')
    def test_successful_post_problem(self):
        job_id = graphhopper.post_problem(problem)
        self.assertEqual(job_id, '86d08bb7-124b-4059-8ae7-e994661211f9')

    @my_vcr.use_cassette('tests/fixtures/vcr_cassettes/graphhopper_error.yaml')
    def test_post_problem_error(self):
        problem = {}
        self.assertRaises(Graphhopper.Error, graphhopper.post_problem, problem)

    @my_vcr.use_cassette('tests/fixtures/vcr_cassettes/graphhopper.yaml')
    def test_get_problem_successful(self):
        job_id = graphhopper.post_problem(problem)
        solution = graphhopper.get_solution(job_id)
        self.assertEqual(solution['job_id'], '86d08bb7-124b-4059-8ae7-e994661211f9')

if __name__ == '__main__':
    unittest.main()
