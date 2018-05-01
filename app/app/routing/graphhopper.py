import requests
from app.app.secret import GRAPHHOPPER_KEY
import json

# gateway to graphhopper route optimization api
class Graphhopper:
    def post_problem(self, problem):
        r = requests.post('https://graphhopper.com/api/1/vrp/optimize?key={0}'.format(GRAPHHOPPER_KEY), json=problem)
        if r.status_code == 200:
            return r.json()['job_id']
        else:
            raise Graphhopper.Error(r.text)

    def get_solution(self, job_id):
        r = requests.get(
            'https://graphhopper.com/api/1/vrp/solution/{job_id}?key={api_key}'.format(
                job_id = job_id,
                api_key = GRAPHHOPPER_KEY))
        if r.status_code == 200:
            return json.loads(r.text)
        else:
            raise Graphhopper.Error(r.text)

    def problem(self):
        return

    class Error(RuntimeError):
        """Any error from the graphhopper API"""