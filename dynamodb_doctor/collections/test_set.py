import pytest 
import aioboto3

from dynamodb_doctor import Model, Set, Int
from dynamodb_doctor.exceptions import MissingAttributeException

ENDPOINT_URL = "http://localhost:58000"

@pytest.mark.asyncio
async def test_save_model_with_set_collection(table_fixture):
    test_set_of_ints = (1,2,3)

    class TestModel(Model):
        set_of_ints = Set(Int)

        class Meta:
            table = table_fixture

    test_model = TestModel(set_of_ints=test_set_of_ints)

    await test_model.save()

    session = aioboto3.Session()
    async with session.resource('dynamodb', endpoint_url=ENDPOINT_URL) as resource:
        table = await resource.Table(table_fixture._name)

        item = await table.get_item(Key={"pk": test_model._pk, "sk": test_model._sk})

        assert("Item" in item)
        set_of_ints = item["Item"]["set_of_ints"]
        for int in set_of_ints:
            assert int in test_set_of_ints

# @pytest.mark.asyncio
# async def test_save_list_string_attribute(table_fixture):
#     class TestModel(Model):
#         names = List(String)

#         class Meta:
#             table = table_fixture

#     names = ["string1", "string2"]
#     test_model = TestModel(names=names)
#     await test_model.save()

#     session = aioboto3.Session()
#     async with session.resource('dynamodb', endpoint_url=ENDPOINT_URL) as resource:
#         table = await resource.Table(table_fixture._name)

#         item = await table.get_item(Key={"pk": test_model._pk, "sk": test_model._sk})

#         assert("Item" in item)
#         assert(item["Item"]["names"] == names)

#     test_models = await TestModel.all()
#     print(test_models)

#     assert(test_models[0].names == names)
#     assert(test_models[0].names != [])
#     assert(test_models[0].names != "string")
#     assert(test_models[0].names != [1, 2])

# @pytest.mark.asyncio
# async def test_save_list_number_attribute_with_list_dict(table_fixture):
#     class TestModel(Model):
#         numbers = List(Int)

#         class Meta:
#             table = table_fixture


#     numbers = [{}]

#     with pytest.raises(AttributeValidationError):
#         _ = TestModel(numbers=numbers)

# @pytest.mark.asyncio
# async def test_save_list_int_attribute(table_fixture):
#     class TestModel(Model):
#         numbers = List(Int)

#         class Meta:
#             table = table_fixture

#     numbers = [1, 2]
#     test_model = TestModel(numbers=numbers)
#     await test_model.save()

#     session = aioboto3.Session()
#     async with session.resource('dynamodb', endpoint_url=ENDPOINT_URL) as resource:
#         table = await resource.Table(table_fixture._name)

#         item = await table.get_item(Key={"pk": test_model._pk, "sk": test_model._sk})

#         assert("Item" in item)
#         assert(item["Item"]["numbers"] == numbers)

#     test_models = await TestModel.all()

#     assert(test_models[0].numbers == numbers)
#     assert(test_models[0].numbers != [])
#     assert(test_models[0].numbers != "string")
#     assert(test_models[0].numbers != ["string1", "string2"])

@pytest.mark.asyncio
async def test_save_model_without_set_attribute(table_fixture):
    class TestModel(Model):
        set_of_ints = Set(Int)

        class Meta:
            table = table_fixture

    with pytest.raises(MissingAttributeException):
        _ = TestModel()