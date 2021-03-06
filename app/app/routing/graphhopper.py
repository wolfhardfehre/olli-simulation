import requests
import json
import time

# gateway to graphhopper route optimization api
class Graphhopper:
    def __init__(self, api_key):
        self.api_key = api_key

    def post_problem(self, problem):
        r = requests.post('https://graphhopper.com/api/1/vrp/optimize?key={0}'.format(self.api_key), json=problem)
        if r.status_code == 200:
            return r.json()['job_id']
        else:
            raise Graphhopper.Error(r.text)

    def get_solution(self, job_id):
        r = self._get_request(job_id)
        if r.status_code == 200:
            result = json.loads(r.text)
            while result.get('status') != 'finished':
                time.sleep(0.5)
                result = json.loads(self._get_request(job_id).text)
            return result.get('solution')
        else:
            raise Graphhopper.Error(r.text)

    def _get_request(self, job_id):
        return requests.get(
                'https://graphhopper.com/api/1/vrp/solution/{job_id}?key={api_key}'.format(
                    job_id = job_id,
                    api_key = self.api_key))

    class Error(RuntimeError):
        """Any error from the graphhopper API"""
