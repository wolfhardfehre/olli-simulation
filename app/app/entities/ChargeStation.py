import pandas as pd


class ChargeStation:

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
                "color": "#E63920",
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
