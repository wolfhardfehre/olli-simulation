import pandas as pd
from shapely.geometry import Point
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from app.app.entities.entity import Entity


class TransportStation(Entity):

    def __init__(self, row):
        self.id = row['id']
        self.type = row['type']
        self.name = row['name']
        self.products = row['products']
        self.lat = row['lat']
        self.lon = row['lon']

    @property
    def point(self):
        return Point(self.lon, self.lat)

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
                "color": "#9966CC",
                "fillOpacity": 0.5,
                "weight": 2,
                "radius": 30,
                "opacity": 0.7
            },
            "properties": {
                "id": self.id,
                "type": self.type,
                "name": self.name,
                "products": self.products
            }
        }

    def __repr__(self):
        return 'TransportStation[id={}, name={}, lat={:.6f}, lon={:.6f}]'.format(
            self.id, self.name, self.lat, self.lon)


if __name__ == '__main__':
    df = pd.read_pickle('./resources/public_transport.p')
    stations = [TransportStation(row) for idx, row in df.iterrows()]
    [print(station) for station in stations]
