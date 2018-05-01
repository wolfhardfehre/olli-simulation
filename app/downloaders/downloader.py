from app.downloaders.graph_downloader import fetch_geometries, GraphDownloader
from app.downloaders.charge_station_downloader import fetch_stations, ChargeStationDownloader
from app.downloaders.public_transport_downloader import fetch_public_transport, PublicTransportDownloader
from app.tools.geo_tools import centroid, meters


class Downloader:
    def __init__(self, bounding_box):
        self.graph_downloader = self.__fetch_graph(bounding_box)
        lon, lat = centroid(bounding_box)
        self.charger_downloader = self.__fetch_chargers(bounding_box, lon, lat)
        self.transport_downloader = self.__fetch_transport(bounding_box, lon, lat)

    def save(self):
        self.graph_downloader.save()
        self.charger_downloader.save()
        self.transport_downloader.save()

    @staticmethod
    def __fetch_graph(bounding_box):
        graph_json = fetch_geometries(bounding_box)
        return GraphDownloader(graph_json)

    @staticmethod
    def __fetch_chargers(bounding_box, lon, lat):
        radius = meters(bounding_box[0], bounding_box[1], lat, lon)
        radius = 1000 if radius < 1000 else radius
        charger_json = fetch_stations(lat, lon, radius)
        return ChargeStationDownloader(charger_json)

    @staticmethod
    def __fetch_transport(bounding_box, lon, lat):
        radius = meters(bounding_box[0], bounding_box[1], lat, lon)
        transport_json = fetch_public_transport(lat, lon, radius)
        return PublicTransportDownloader(transport_json)


if __name__ == '__main__':
    NORTH = 52.4872472
    SOUTH = 52.479951
    WEST = 13.352029
    EAST = 13.359325
    downloader = Downloader([SOUTH, WEST, NORTH, EAST])
    downloader.save()
