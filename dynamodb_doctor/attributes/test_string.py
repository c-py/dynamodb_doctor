import pytest 
import aioboto3

from dynamodb_doctor import Model, String, MissingAttributeException

ENDPOINT_URL = "http://localhost:58000"

@pytest.mark.asyncio
async def test_save_model_with_string_attribute(table_fixture):
    test_model_name = "test_model"

    class TestModel(Model):
        name = String()

        class Meta:
            table = table_fixture

    test_model = TestModel(name=test_model_name)

    await test_model.save()

    session = aioboto3.Session()
    async with session.resource('dynamodb', endpoint_url=ENDPOINT_URL) as resource:
        table = await resource.Table(table_fixture._name)

        item = await table.get_item(Key={"pk": test_model._pk, "sk": test_model._sk})

        assert("Item" in item)
        assert(item["Item"]["name"] == test_model_name)

@pytest.mark.asyncio
async def test_save_model_without_string_attribute(table_fixture):
    class TestModel(Model):
        name = String()

        class Meta:
            table = table_fixture

    with pytest.raises(MissingAttributeException):
        _ = TestModel()