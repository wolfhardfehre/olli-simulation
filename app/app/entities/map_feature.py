import abc


class MapFeature:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.highlight_color = "#FFFFFF"
        self.__normal = None
        self.__highlighted = None

    def to_geojson(self):
        if self.__normal is None:
            self.__normal = {
                "type": "Feature",
                "geometry": self._geometry(),
                "style": self._style(),
                "properties": self._properties()
            }
        return self.__normal

    def highlight(self):
        if self.__highlighted is None:
            self.__highlighted = {
                "type": "Feature",
                "geometry": self._geometry(),
                "style": self._highlight_style(),
                "properties": self._properties()
            }
        return self.__highlighted

    @abc.abstractmethod
    def _geometry(self):
        NotImplementedError()

    @abc.abstractmethod
    def _style(self):
        NotImplementedError()

    @abc.abstractmethod
    def _highlight_style(self):
        NotImplementedError()

    @abc.abstractmethod
    def _properties(self):
        NotImplementedError()
