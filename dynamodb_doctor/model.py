from typing import Any, Dict, List as ListTyping
from ksuid import ksuid

from dynamodb_doctor.table import Table
from dynamodb_doctor.attributes.attribute import Attribute
from dynamodb_doctor.collections.collection import Collection
from dynamodb_doctor.exceptions import ModelCreationException, MissingAttributeException, DeserializationException

class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        parents = [base for base in bases if isinstance(base, ModelMeta)]
        if not parents:
            return super().__new__(cls, name, bases, attrs)

        model = super().__new__(cls, name, bases, attrs)

        if (not hasattr(model, "Meta")
            or not hasattr(model.Meta, "table") 
            or not isinstance(model.Meta.table, Table)
        ):
            raise ModelCreationException()

        model._table = model.Meta.table
        model._attributes = {}
        model._relationships = {}


        for k, v in attrs.items():

            if issubclass(type(v), (Attribute, Collection)):
                model._attributes[k] = v

            if issubclass(type(v), (Relationship)):
                model._relationships[k] = v

        if hasattr(model, "Meta") and hasattr(model.Meta, "name"):
            setattr(model, "_name", model.Meta.name)
        else:
            setattr(model, "_name", name.lower())

        model._table.register_model(model._name, model)
        model._pk = model._name

        return model

class Model(metaclass=ModelMeta):
    def __init__(self, **kwargs):
        if "sk" in kwargs and isinstance(kwargs["sk"], str):
            self._sk = kwargs["sk"]
        else:
            self._sk = str(ksuid())

        for attribute_name, attribute in self._attributes.items():
            if attribute_name not in kwargs.keys():
                raise MissingAttributeException(attribute_name)
            else:
                attribute.set(kwargs[attribute_name])

        for relationship_name, relationship in self._relationships.items():
            if relationship_name in kwargs.keys():
                relationship.set(kwargs[relationship_name])

    def __repr__(self):
        return str(self._serialize())

    @classmethod
    async def _deserialize(cls, *, item: Dict[Any, Any]) -> "Model":
        if (model_cls := cls._table.lookup_model(item.get("pk"))):
            return model_cls(**item)
        raise DeserializationException()


    def _serialize(
        self,
        *,
        prefix: str = ""
    ) -> ListTyping[Dict[Any, Any]]:
        """
        Takes a DynamoDB Doctor model returns a list of items to persist in DynamoDB
        """
        items = []

        item_id = f"{self.type}#{self.id}"
        item = {
            "pk": self.type,
            "sk": self.id,
            "gsi1_pk": "dummy",
            "gsi2_pk": f"{prefix}{item_id}"
        }

        for attribute_name, attribute in self._attributes.items():
            item[attribute_name] = attribute.get()

        for relationship in self._relationships.values():
            items.extend(relationship._serialize(prefix=prefix))

        items.append(item)
        return items

    async def save(self):
        """
        Saves a model to DynamoDB.
        """
        items = self._serialize()
        await self._table.batch_put_items(items=items)

    @property
    def id(self):
        """
        The ID of the entity.
        """
        return self._sk

    @property
    def type(self):
        """
        The Type of the entity.
        """
        return self._pk

    @classmethod
    async def all(cls):
        """
        Query for all instances of the model.
        """
        _models = await cls._table.query_by_pk(cls._pk)
        return [await cls._deserialize(item=_model) for _model in _models]

from dynamodb_doctor.relationships.many import Many
from dynamodb_doctor.relationships.relationship import Relationship
