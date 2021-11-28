from typing import Any, Dict, List as ListTyping

from .relationship import Relationship

from dynamodb_doctor.model import Model
from dynamodb_doctor.relationships.exceptions import RelationshipValidationException


class Many(Relationship):
    def __init__(self, model):
        if not issubclass(model, Model):
            raise RelationshipValidationException()
        self._model = model

        self._model_instances = []

    def add(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], dict):
            model_kwargs = args[0]
        else:
            model_kwargs = kwargs

        self._model_instances.append(self._model(**model_kwargs))

    def set(self, value):
        if not hasattr(value, '__iter__'):
            raise RelationshipValidationException()

        for v in value:
            self.add(v)

    def get(self):
        ...

    def __len__(self):
        return len(self._model_instances)

    def __getitem__(self, item):
        return self._model_instances[item]

    def __repr__(self):
        return str(self._model_instances)

    def _serialize(self, *, prefix: str = "") -> ListTyping[Dict[Any, Any]]:
        items = []

        for model_instance in self._model_instances:
            items.extend(model_instance._serialize(prefix=prefix))
  
        return items

    