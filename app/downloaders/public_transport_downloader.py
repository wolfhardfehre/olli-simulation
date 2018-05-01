import requests
import pandas as pd


BASE_URL = 'https://2.vbb.transport.rest/stations/nearby'


def fetch_public_transport(lat, lon, radius, results=10):
    """
    Fetch public transport stations.
    e.g. https://2.vbb.transport.rest/stations/nearby?latitude=52.52725&longitude=13.4123

    Parameters
    ----------
    lat: float
        latitude in degrees
    lon: float
        longitude in degrees
    radius: int
        radius in meters
    results: int
        number of maximum results

    Returns
    -------
    json: containing the charge stations

    """
    headers = {'X-Identifier': 'olli-simulation'}
    params = {'latitude': lat, 'longitude': lon, 'distance': radius, 'results': results}
    response = requests.get(url=BASE_URL, params=params, headers=headers)
    return response.json()


class PublicTransportDownloader:

    def __init__(self, json):
        self.stations = self.__build_stations(json)

    def __build_stations(self, json):
        df = pd.DataFrame(columns=['id', 'type', 'name', 'lat', 'lon', 'products', 'distance'])
        for station in json:
            df = df.append(self.__to_row(station), ignore_index=True)
        return df

    @staticmethod
    def __to_row(station):
        location = station['location']
        lon, lat = location['longitude'], location['latitude']
        return {'id': station['id'],
                'type': station['type'],
                'name': station['name'],
                'lat': lat,
                'lon': lon,
                'products': [mode for mode, exists in station['products'].items() if exists],
                'distance': station['distance']
        }

    def save(self):
        print('** Public Transport Stations **')
        print(self.stations)
        self.stations.to_pickle('./resources/public_transport.p')


if __name__ == '__main__':
    js = fetch_public_transport(52.481528, 13.356441, 1000)
    downloader = PublicTransportDownloader(js)
    downloader.save()
