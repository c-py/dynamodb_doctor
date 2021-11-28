import pytest 

from dynamodb_doctor import Model, String, ModelCreationException, Many

ENDPOINT_URL = "http://localhost:58000"

@pytest.mark.asyncio
async def test_define_model_without_table():
    with pytest.raises(ModelCreationException):
        class _(Model):
            name = String()


@pytest.mark.asyncio
async def test_list_all(table_fixture):
    test_model_name = "test_model"

    class TestModel(Model):
        name = String()

        class Meta:
            table = table_fixture

    test_model = TestModel(name=test_model_name)

    await test_model.save()

    test_models = await TestModel.all()

    assert(len(test_models) == 1)
    assert(test_models[0].id == test_model.id)

@pytest.mark.asyncio
async def test_list_one_to_many(table_fixture):
    class TestModelMany(Model):
        name = String()

        class Meta:
            table = table_fixture

    class TestModelOne(Model):
        title = String()
        many = Many(TestModelMany)

        class Meta:
            table = table_fixture

    test_model_one = TestModelOne(
        title="test",
        many=[{"name":"testone"}, {"name":"testtwo"}]
    )

    await test_model_one.save()

    test_models = await TestModelOne.all()

    assert(len(test_models) == 1)

    one = test_models[0]
    assert(one.id == test_model_one.id)

    many = test_models[0].many
    assert(len(many) == 2)
    
    assert(many[0].name == "testone")
    assert(many[1].name == "testtwo")
