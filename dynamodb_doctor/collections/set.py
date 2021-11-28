from .collection import Collection

from dynamodb_doctor.attributes.attribute import Attribute
from dynamodb_doctor.attributes.exceptions import AttributeValidationError

class Set(Collection):
    def __init__(self, attribute):
        if not issubclass(attribute, Attribute):
            raise AttributeValidationError()

        self._attribute = attribute        

    def __eq__(self, other):
        if not hasattr(other, '__iter__'):
            return False

        if len(self.values) != len(other):
            return False

        return all(self.values[i].get() == element for i, element in enumerate(other))

    def __len__(self):
        return len(self.values)

    def set(self, values):
        if not hasattr(values, '__iter__'):
            raise AttributeValidationError()

        self.values = set()

        for value in values:
            attr = self._attribute()
            attr.set(value)
            self.values.add(attr)

    def get(self):
        return {v.get() for v in self.values}