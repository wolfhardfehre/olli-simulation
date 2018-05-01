import pandas as pd
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from app.app.entities.entity import Entity


class ChargeStation(Entity):

    def __init__(self, row):
        self.id = row['id']
        self.name = row['name']
        self.data_type = row['data_type']
        self.lat = row['lat']
        self.lon = row['lon']

    def to_geojson(self):
        return {
            "geometry": {
                "type": "Point",
                "coordinates": [
                    self.lon, self.lat
                ]
            },
            "type": "Feature",
            "style": {
                "color": "#fccf40",
                "fillOpacity": 0.5,
                "weight": 2,
                "radius": 20,
                "opacity": 0.7
            },
            "properties": {
                "id": self.id,
                "name": self.name,
                "data_type": self.data_type
            }
        }

    def __repr__(self):
        return 'ChargeStation[id={}, name={}, lat={:.6f}, lon={:.6f}]'.format(
            self.id, self.name, self.lat, self.lon)


if __name__ == '__main__':
    df = pd.read_pickle('./resources/charge_stations.p')
    stations = [ChargeStation(row) for idx, row in df.iterrows()]
    [print(station) for station in stations]
