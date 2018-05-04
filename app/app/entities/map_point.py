import abc

from app.app.entities.map_feature import MapFeature


class MapPoint(MapFeature):
    __metaclass__ = abc.ABCMeta

    def __init__(self, lat, lon):
        super().__init__()
        self.lat = lat
        self.lon = lon

    def _geometry(self):
        return {
            "type": "Point",
            "coordinates": [self.lon, self.lat]
        }

    def _highlight_style(self):
        return {
            "color": self.highlight_color,
            "fillOpacity": 0.5,
            "weight": 2,
            "radius": 20,
            "opacity": 0.7
        }

    @abc.abstractmethod
    def _style(self):
        NotImplementedError()

    @abc.abstractmethod
    def _properties(self):
        NotImplementedError()