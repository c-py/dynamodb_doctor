import pytest 
import aioboto3

from dynamodb_doctor import Model, String, List

ENDPOINT_URL = "http://localhost:58000"

@pytest.mark.asyncio
async def test_list_string(table_fixture):
    class TestModel(Model):
        names = List(String)

        class Meta:
            table = table_fixture

    names = ["string1", "string2"]
    test_model = TestModel(names=names)
    await test_model.save()

    test_models = await TestModel.all()
    assert(test_models[0].names == names)