from sqlalchemy import and_
from sqlalchemy.sql import select
import pandas as pd
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))
from app.app.models import VehicleStates
from app.app.app import db


class AnimateGenerator:
    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = AnimateGenerator()
        return cls.instance

    def __init__(self, start_time='2018-02-14 15:40:00', end_time='2018-02-14 16:05:00'):
        data_frame = self.__get_data_frame(start_time, end_time)
        self.animation_data = data_frame.iterrows()

    def next(self):
        row = next(self.animation_data)[1]
        return self.to_geojson(row)

    def to_geojson(self, row):
        return {
            "geometry": {
                "type": "Point",
                "coordinates": [
                    row['longitude'], row['latitude']
                ]
            },
            "type": "Feature",
            "properties": self.__properties(row)
        }

    @staticmethod
    def __properties(row):
        return {
            "vehicle_id": row["vehicle_id"],
            "theta": row["theta"],
            "speed": row["speed"],
            "last_seen": row["last_seen"],
            "created_at": row["created_at"],
            "battery": row['battery']
        }

    @staticmethod
    def __get_data_frame(start_time, end_time):
        query = select([VehicleStates]) \
            .where(
                and_(
                    VehicleStates.last_seen > start_time,
                    VehicleStates.last_seen < end_time
                )
            )
        return pd.read_sql_query(sql=query, con=db.engine, parse_dates=['last_seen', 'created_at'])
