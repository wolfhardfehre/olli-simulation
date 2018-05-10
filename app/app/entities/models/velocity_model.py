import random


class VelocityModel:
    def __init__(self, min_speed=3.0, max_speed=3.0):
        """
        Sets the minimum and the maximum for the speed model.

        Parameters
        ----------
        min_speed: float
            minimum speed in meters per second
        max_speed: float
            maximum speed in meters per second
        """
        self.min_speed = min_speed
        self.max_speed = max_speed

    def current_velocity(self):
        """
        Get current random velocity in meters per second.

        Returns
        -------
        float velocity in meters per second

        """
        return random.uniform(self.min_speed, self.max_speed)
