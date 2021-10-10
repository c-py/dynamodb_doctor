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
        if hasattr(self, "Meta") and hasattr(self.Meta, "name"):
            setattr(self, "_name", self.Meta.name)
        else:
            # TODO convert name into snake case
            setattr(self, "_name", self.__class__.__name__.lower())

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
                BillingMode='PAY_PER_REQUEST'
            )

            waiter = client.get_waiter('table_exists')
            await waiter.wait(TableName=self._name)

    async def put_item(self, **kwargs):
        session = aioboto3.Session()
        async with session.resource('dynamodb', endpoint_url=getattr(self.Meta, "endpoint_url")) as resource:
            table = await resource.Table(self._name)
            # TODO Batch put_item
            await table.put_item(**kwargs)

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