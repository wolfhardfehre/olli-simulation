import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../..")))
from app.app.routing.graph import Graph
from app.app.entities.models.velocity_model import VelocityModel
from app.app.entities.models.battery_model import BatteryModel
from app.app.entities.round_trip_shuttle import RoundTripShuttle


class RoundTripGenerator:
    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = RoundTripGenerator()
        return cls.instance

    def __init__(self):
        self.time = 0.0
        self.shuttle = RoundTripShuttle(Graph.load_default(),
                                        self.time,
                                        VelocityModel(),
                                        BatteryModel())

    def next(self):
        self.time += 1
        self.shuttle.move(self.time)
        return self.shuttle.to_geojson()

    def current_ground_data(self):
        return {
            "type": "FeatureCollection",
            "features": self.shuttle.get_ground_data()
        }
