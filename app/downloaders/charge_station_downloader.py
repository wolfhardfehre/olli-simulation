import requests
import pandas as pd


BASE_URL = 'http://data.datarun2018.de/EVCharging/stations'


def fetch_stations(lat, lon, radius, detail='low'):
    """
    Fetch charging stations around a certain coordinate within a specified radius.
    e.g. http://data.datarun2018.de/EVCharging/stations?lat=52.4590335&lng=13.3738759&radius=20000&detail=low

    Parameters
    ----------
    lat: float
        latitude in degrees
    lon: float
        longitude in degrees
    radius: int
        radius in meters
    detail: str
        either 'low' or 'high' for level of detail

    Returns
    -------
    json: containing the charge stations

    """
    params = {'lat': lat, 'lng': lon, 'radius': radius, 'detail': detail}
    response = requests.get(url=BASE_URL, params=params)
    return response.json()


class ChargeStationDownloader:

    def __init__(self, json):
        self.charge_stations = self.__build_stations(json)
        print(self.charge_stations)

    def __build_stations(self, json):
        df = pd.DataFrame(columns=['id','name', 'data_type', 'lat', 'lon'])
        for station in json:
            df = df.append(self.__to_row(station), ignore_index=True)
        return df

    @staticmethod
    def __to_row(station):
        lon, lat = station['location']['coordinates']
        return {'id': station['id'],
                'name': station['name'],
                'data_type': station['dataType'],
                'lat': lat,
                'lon': lon}

    def save(self):
        self.charge_stations.to_pickle('./resources/charge_stations.p')


if __name__ == '__main__':
    js = fetch_stations(52.481528, 13.356441, 20000)
    downloader = ChargeStationDownloader(js)
    downloader.save()
