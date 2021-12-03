from abc import ABC, abstractmethod

class AttributeInstance(ABC):
    @abstractmethod
    def __init__(self, validate_fn, value):
        ...

    @abstractmethod
    def __repr__(self) -> str:
        ...
        
    @abstractmethod
    def __eq__(self, other) -> bool:
        ... 

class Attribute(ABC):
    @abstractmethod
    def new(self, value) -> AttributeInstance:
        ...