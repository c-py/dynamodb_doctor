from .attribute import Attribute
from .exceptions import AttributeValidationError

class String(Attribute):
    def set(self, value):
        if not isinstance(str(value), str):
            raise AttributeValidationError()

        self.value = str(value)

    def get(self):
        return self.value

    def __repr__(self) -> str:
        return self.get()