from .attribute import Attribute, AttributeInstance
from .exceptions import AttributeValidationError

class StringInstance(AttributeInstance):
    def __init__(self, validate_fn, value):
        self.validate_fn = validate_fn
        self.validate_fn(value)
        self.value = value

    def get(self):
        return self.value

    def __repr__(self) -> str:
        return self.get()

    def __eq__(self, other) -> bool:
        return self.get() == other

class String(Attribute):
    def new(self, value):

        def validate_fn(v):
            if not isinstance(str(v), str):
                raise AttributeValidationError()

        return StringInstance(validate_fn, value)
