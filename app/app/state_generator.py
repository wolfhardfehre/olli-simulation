import models
from app import db
from sqlalchemy import and_
from sqlalchemy.sql import select
import pandas as pd


class StateGenerator:
    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = StateGenerator()
        return cls.instance

    def __init__(self, start_time='2018-02-14 15:40:00', end_time='2018-02-14 16:05:00'):
        dataframe = self.__get_dataframe(start_time, end_time)
        self.animation_data = dataframe.iterrows()

    def next_coordinate(self):
        row = next(self.animation_data)[1]
        return row['longitude'], row['latitude']

    @staticmethod
    def __get_dataframe(start_time, end_time):
        query = select([models.VehicleStates]) \
            .where(
                and_(
                    models.VehicleStates.last_seen > start_time,
                    models.VehicleStates.last_seen < end_time
                )
            )
        return pd.read_sql_query(sql=query, con=db.engine, parse_dates=['last_seen', 'created_at'])
