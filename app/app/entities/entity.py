import abc


class Entity:
    __metaclass__ = abc.ABCMeta

    def __init__(self, graph, time):
        self.graph = graph.graph
        self.time = time

    @abc.abstractmethod
    def move(self, current_time):
        NotImplementedError()
