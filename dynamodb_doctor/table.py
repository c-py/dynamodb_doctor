from typing import Any, Optional
import aioboto3
from boto3.dynamodb.conditions import Key

class TableMeta(type):
    def __new__(cls, clsname, superclasses, attributedict):
        parents = [sc for sc in superclasses if isinstance(sc, TableMeta)]
        if not parents:
            return super().__new__(cls, clsname, superclasses, attributedict)

        table = super().__new__(cls, clsname, superclasses, attributedict)

        return table

class Table(metaclass=TableMeta):
    def __init__(self):
        self._models = {}

        if hasattr(self, "Meta") and hasattr(self.Meta, "name"):
            setattr(self, "_name", self.Meta.name)
        else:
            # TODO convert name into snake case
            setattr(self, "_name", self.__class__.__name__.lower())

    def register_model(self, name, cls) -> None:
        self._models[name] = cls

    def lookup_model(self, name) -> Optional[type[Any]]:
        return self._models.get(name)

    async def create(self):
        session = aioboto3.Session()
        async with session.client('dynamodb', endpoint_url=getattr(self.Meta, "endpoint_url")) as client:
            await client.create_table(
                TableName=self._name,
                AttributeDefinitions=[
                    {
                        'AttributeName': 'pk',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'sk',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'gsi1_pk',
                        'AttributeType': 'S'
                    },
                    {
                        'AttributeName': 'gsi1_sk',
                        'AttributeType': 'S'
                    },
                ],
                KeySchema=[
                    {
                        'AttributeName': 'pk',
                        'KeyType': 'HASH'
                    },
                    {
                        'AttributeName': 'sk',
                        'KeyType': 'RANGE'
                    },
                ],
                BillingMode='PAY_PER_REQUEST',
                GlobalSecondaryIndexes=[
                    {
                        'IndexName': 'gsi1',
                        'KeySchema': [
                            {
                                'AttributeName': 'gsi1_pk',
                                'KeyType': 'HASH'
                            },
                            {
                                'AttributeName': 'gsi1_sk',
                                'KeyType': 'RANGE'
                            },
                        ],
                        'Projection': {
                            'ProjectionType': 'ALL'
                        }
                    }
                ]
            )

            waiter = client.get_waiter('table_exists')
            await waiter.wait(TableName=self._name)

    async def batch_put_items(self, *, items):
        session = aioboto3.Session()
        async with session.resource('dynamodb', endpoint_url=getattr(self.Meta, "endpoint_url")) as resource:
            table = await resource.Table(self._name)

            async with table.batch_writer() as batch:
                for item in items:
                    await batch.put_item(Item=item)

    async def query_by_pk(self, pk: str):
        session = aioboto3.Session()
        async with session.resource('dynamodb', endpoint_url=getattr(self.Meta, "endpoint_url")) as resource:
            table = await resource.Table(self._name)

            kwargs = {
                "KeyConditionExpression": Key('pk').eq(pk),
                "ScanIndexForward": False,
            }
            response = await table.query(**kwargs)
            items = response["Items"]
            while "LastEvaluatedKey" in response:
                response = await table.query(
                    **kwargs, ExclusiveStartKey=response["LastEvaluatedKey"]
                )
                items.extend(response["Items"])

            return items