import uuid

from dynamodb_doctor.table import Table
from dynamodb_doctor.attributes import String, Int, List
from dynamodb_doctor.exceptions import ModelCreationException, MissingAttributeException

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

        for k, v in attrs.items():
            if isinstance(v, (String, Int, List)):
                model._attributes[k] = v

        if hasattr(model, "Meta") and hasattr(model.Meta, "name"):
            setattr(model, "_name", model.Meta.name)
        else:
            setattr(model, "_name", name.lower())
        model._pk = model._name

        return model

class Model(metaclass=ModelMeta):
    def __init__(self, **kwargs):
        if "sk" in kwargs and isinstance(kwargs["sk"], str):
            self._sk = kwargs["sk"]
        else:
            # TODO ksuid
            self._sk = str(uuid.uuid4())

        for attribute_name, attribute in self._attributes.items():
            if attribute_name not in kwargs.keys():
                raise MissingAttributeException()
            else:
                attribute.set(kwargs[attribute_name])

    async def save(self):
        await self._table.put_item(Item={
            "pk": self._pk, 
            "sk": self._sk, 
            **{attribute_name: attribute.get() for attribute_name, attribute in self._attributes.items()}
        })

    @property
    def id(self):
        return self._sk

    @classmethod
    async def all(cls):
        _models = await cls._table.query_by_pk(cls._pk)
        return [cls(**_model) for _model in _models]