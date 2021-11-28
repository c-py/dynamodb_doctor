from abc import ABC, abstractmethod

class Collection(ABC):
    @abstractmethod
    def __init__(self, attribute):
        ...
        
    @abstractmethod
    def set(self, value):
        ...

    @abstractmethod
    def get(self):
        ...