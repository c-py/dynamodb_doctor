from .collection import Collection, CollectionInstance

from dynamodb_doctor.attributes.attribute import Attribute
from dynamodb_doctor.attributes.exceptions import AttributeValidationError

class SetInstance(CollectionInstance):
    def __init__(self, attribute, validation_fn, values = []):
        self._attribute = attribute
        self.validation_fn = validation_fn
        self.validation_fn(values)

        self.values = set()
        for value in values:
            attr = self._attribute.new(value)
            self.values.add(attr)

    def __repr__(self):
        return str({v.get() for v in self.values})

    def __eq__(self, other):
        if not hasattr(other, '__iter__'):
            return False

        if len(self.values) != len(other):
            return False

        return all(self.values[i].get() == element for i, element in enumerate(other))

    def __len__(self):
        return len(self.values)

    def get(self):
        return {v.get() for v in self.values}

class Set(Collection):
    def __init__(self, attribute):
        self._attribute = attribute

    def new(self, values = []):

        def validate_fn(v):
            if not isinstance(self._attribute, Attribute):
                raise AttributeValidationError()

            if not hasattr(v, '__iter__'):
                raise AttributeValidationError()    

        return SetInstance(self._attribute, validate_fn, values)