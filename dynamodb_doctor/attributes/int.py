from .attribute import Attribute
from .exceptions import AttributeValidationError

class Int(Attribute):
    def set(self, value):
        if not isinstance(int(value), int):
            raise AttributeValidationError()

        self.value = value

    def get(self):
        return self.value
