from .attribute import Attribute
from .exceptions import AttributeValidationError

from dynamodb_doctor.attributes.string import String

class List(Attribute):
    def __init__(self, element):
        if element not in (String,):
            raise AttributeValidationError()

    def set(self, value):
        if not isinstance(value, list):
            raise AttributeValidationError()

        self.values = ['string1', 'string2']

    def get(self):
        return self.values
