import requests
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import WKTElement


BASE_URL = 'http://data.datarun2018.de/EVCharging/stations'


engine = create_engine('postgresql:///open_olli', echo=False)
Base = declarative_base(engine)
Session = sessionmaker(bind=engine)
session = Session()


def fetch_stations(lat, lon, radius, detail='low'):
    params = {
        'lat': lat,
        'lng': lon,
        'radius': radius,
        'detail': detail
    }
    response = requests.get(url=BASE_URL, params=params)
    return response.json()


class ChargeStation(Base):
    """Mapping for charge stations data (existing table)"""
    __tablename__ = 'charge_stations'
    __table_args__ = {'autoload': True}


if __name__ == '__main__':
    json = fetch_stations(52.481528, 13.356441, 20000)
    for station in json:
        lng, lat = station['location']['coordinates']
        wkt = WKTElement('POINT({} {})'.format(lng, lat), 4326)
        session.add(ChargeStation(data_type=station['dataType'], name=station['name'], geometry=wkt))
    session.commit()
