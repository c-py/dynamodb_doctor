from .attribute import Attribute
from .exceptions import AttributeValidationError

class Int(Attribute):
    def set(self, value):
        try:
            int(value)
        except TypeError:
            raise AttributeValidationError()            

        self.value = int(value)

    def get(self):
        return self.value
