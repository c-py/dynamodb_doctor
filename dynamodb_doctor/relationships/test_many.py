import pytest 
import aioboto3

from dynamodb_doctor import Model, String, Many
from dynamodb_doctor.exceptions import MissingAttributeException

ENDPOINT_URL = "http://localhost:58000"

@pytest.mark.asyncio
async def test_model_with_many_to_model_relationship(table_fixture):
    class TestModelA(Model):
        name = String()

        class Meta:
            table = table_fixture

    class TestModelB(Model):
        relation = Many(TestModelA)

        class Meta:
            table = table_fixture

    test_model = TestModelB()

    await test_model.save()

    session = aioboto3.Session()
    async with session.resource('dynamodb', endpoint_url=ENDPOINT_URL) as resource:
        table = await resource.Table(table_fixture._name)

        item = await table.get_item(Key={"pk": test_model._pk, "sk": test_model._sk})

        assert("Item" in item)

@pytest.mark.asyncio
async def test_can_add_to_model_with_many_relationship(table_fixture):
    class TestModelA(Model):
        name = String()

        class Meta:
            table = table_fixture

    class TestModelB(Model):
        relation = Many(TestModelA)

        class Meta:
            table = table_fixture

    test_model = TestModelB()
    test_model.relation.add(name="number1")
    test_model.relation.add({"name": "number2"})

    await test_model.save()

    test_models = await TestModelB.all()

    assert(len(test_models) == 1)
    assert(len(test_models[0].relation) == 2)

    assert test_models[0].relation[0].name == "number1" 
    assert test_models[0].relation[1].name == "number2" 


@pytest.mark.asyncio
async def test_model_with_many_to_attribute_relationship_fails(table_fixture):
    ...