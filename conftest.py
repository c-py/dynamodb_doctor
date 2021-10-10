import pytest
import os
import random 
import string

from dynamodb_doctor import Table

ENDPOINT_URL = "http://localhost:58000"

@pytest.fixture(autouse=True)
def setup():
    key = ''.join(random.choices(string.ascii_letters, k=8))
    os.environ.update({"AWS_ACCESS_KEY_ID": key, "AWS_SECRET_ACCESS_KEY": key})

@pytest.fixture
async def table_fixture():
    class FixtureTable(Table):
        class Meta:
            endpoint_url = ENDPOINT_URL

    table = FixtureTable()
    await table.create()
    return table
