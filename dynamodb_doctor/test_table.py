import pytest
import aioboto3

from dynamodb_doctor import Table

ENDPOINT_URL = "http://localhost:58000"

@pytest.mark.asyncio
async def test_create_table_with_default_name():
    default_name = "test"

    class Test(Table):
        class Meta:
            endpoint_url = ENDPOINT_URL

    table = Test()
    await table.create()

    session = aioboto3.Session()
    async with session.client('dynamodb', endpoint_url=ENDPOINT_URL) as client:
        table = await client.describe_table(TableName=default_name)

        assert(table["Table"]["KeySchema"] == [
            {
                'AttributeName': 'pk',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'sk',
                'KeyType': 'RANGE'
            }
        ])


@pytest.mark.asyncio
async def test_create_table_with_custom_name():
    custom_name = "custom"

    class Test(Table):
        class Meta:
            endpoint_url = ENDPOINT_URL
            name = custom_name

    table = Test()
    await table.create()

    session = aioboto3.Session()
    async with session.client('dynamodb', endpoint_url=ENDPOINT_URL) as client:
        table = await client.describe_table(TableName=custom_name)

        assert(table["Table"]["KeySchema"] == [
            {
                'AttributeName': 'pk',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'sk',
                'KeyType': 'RANGE'
            }
        ])
