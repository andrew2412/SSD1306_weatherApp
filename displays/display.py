import abc

class display(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def getSize(self):
        pass

    @abc.abstractmethod
    def draw(self, image):
        pass

    