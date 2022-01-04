# DynamoDB Doctor

The DynamoDB doctor helps to model common relationships and access patterns in DynamoDB.

## Features

| Feature        | Implemented |
| ---            | ---         |
| Create Tables  | ✅          | 
| Create Models  | ✅          |

## Usage

### Creating a Table

```py
class ExampleTable(Table):
    ...

table = ExampleTable()
table.create()
```

#### Specifying Table Name

```py
class ExampleTable(Table):
    name = "example_table"
```

### Creating a Model

```py
class ExampleTable(Table):
    ...

table = ExampleTable()

class ExampleModel(Model):
    name = String()
    age = Int()

    class Meta:
        table = table
```

## Contributing

### Installation

`make install`

### Testing

`make test`