import random
from app.app.entities.shuttle import LATITUDE_APPROX


class VelocityModel:
    def __init__(self, min_speed=10.0, max_speed=10.0):
        self.min_speed = min_speed
        self.max_speed = max_speed

    def current_velocity(self):
        """Current random velocity in degrees per second"""
        return random.uniform(self.min_speed, self.max_speed) / LATITUDE_APPROX
