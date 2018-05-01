import abc


class Entity:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def to_geojson(self):
        NotImplementedError()
