from abc import ABC, abstractmethod

class Relationship(ABC):
    @abstractmethod
    def __init__(self, model):
        ...

    @abstractmethod
    def set(self, value):
        ...

    @abstractmethod
    def get(self):
        ...