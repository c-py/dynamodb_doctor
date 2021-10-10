from abc import ABC, abstractmethod

class Attribute(ABC):
    @abstractmethod
    def set(self, value):
        ...

    @abstractmethod
    def get(self):
        ...