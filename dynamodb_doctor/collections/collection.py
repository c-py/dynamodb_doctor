from abc import ABC, abstractmethod

class CollectionInstance(ABC):
    @abstractmethod
    def __init__(self, attribute, validate_fn, values):
        ...

    @abstractmethod
    def __repr__(self) -> str:
        ...
        
    @abstractmethod
    def __eq__(self, other) -> bool:
        ... 

    @abstractmethod
    def __len__(self) -> int:
        ...

class Collection(ABC):
    @abstractmethod
    def __init__(self, attribute):
        ...

    @abstractmethod
    def new(self, values) -> CollectionInstance:
        ...