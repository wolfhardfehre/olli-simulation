import abc


class Story:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_type(self):
        NotImplementedError()
        
    @abc.abstractmethod
    def has_ended(self):
        NotImplementedError()

    @abc.abstractmethod
    def update(self, time):
        NotImplementedError()