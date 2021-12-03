from .attribute import Attribute, AttributeInstance
from .exceptions import AttributeValidationError

class IntInstance(AttributeInstance):
    def __init__(self, validate_fn, value):
        self.validate_fn = validate_fn
        self.validate_fn(value)
        self.value = value

    def get(self) -> int:
        return self.value

    def __repr__(self) -> str:
        return str(self.get())

    def __eq__(self, other) -> bool:
        return self.get() == other

    def __hash__(self) -> int:
        return self.get()

class Int(Attribute):
    def new(self, value):

        def validate_fn(v):
            try:
                int(v)
            except TypeError:
                raise AttributeValidationError()            

        return IntInstance(validate_fn, value)
