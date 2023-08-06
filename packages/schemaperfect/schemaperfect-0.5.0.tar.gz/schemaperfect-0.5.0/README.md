![schemaperfect logo](https://user-images.githubusercontent.com/10873576/92287170-f3dd4c80-eed6-11ea-81e4-2037d8a1e555.png)

# schemaperfect

Auto-generate Python APIs from JSON schema specifications

[![build status](http://img.shields.io/travis/jwilson8767/schemaperfect/master.svg?style=flat)](https://travis-ci.org/jwilson8767/schemaperfect)


## About

[JSON Schema](http://json-schema.org/) is a vocabulary that allows you to
annotate and validate JSON documents.

``schemaperfect`` lets you auto-generate simple Python object-based APIs given a valid JSON schema specification. 

This is a living fork of the (now abandoned) [project "schemapi" by altair-viz](https://github.com/altair-viz/schemapi).


## Simple Example

As a very simple example, imagine you have the following simple JSON schema,
defined as a Python dictionary:

```python
schema = {
  'properties': {
    'name': {'type': 'string'},
    'age': {'type': 'integer'}
  }
}
```

This schema specifies that a data instance is valid if it has a key "name" that
maps to a string, and a key "age" that maps to an integer.
So, for example, this dictionary would be valid:

```python
valid = {'name': 'suzie', 'age': 32}
```

while this dictionary would not:

```python
invalid = {'name': 'suzie', 'age': 'old'}
```


### Validation with ``jsonschema``


In Python, you can use the ``jsonschema`` package (which is installed with schemaperfect automatically) to validate any data objects against this schema. For example, this data passes:

```python
jsonschema.validate(valid, schema)
```

While this data fails, as indicated by the ``ValidationError``:

```python
jsonschema.validate(invalid, schema) # raises ValidationError: 'old' is not of type 'integer'
```

### API Generation

The ``schemaperfect`` package lets you generate a Python API that allows you to build
up this kind of data not with raw dictionaries, but with an object-oriented
Python approach.

For example, here is how you can create a local module named ``myschema`` that
includes an object hierarchy designed for creating and validating data under
this schema:

```python
import schemaperfect

api = schemaperfect.SchemaModuleGenerator(schema, root_name='Person')
api.write_module('myschema.py')
```

The result of this is that a new Python module named ``myschema.py`` is written
to disk in the local directory; we can import the root object and use it to construct
some data:

```python
from myschema import Person

person = Person(name='suzie', age=32)
```

This data can be output in the form of a JSON dict:

```python
person.to_dict() # {'age': 32, 'name': 'suzie'}
```

The object can also be instantiated from a dict:

```python
person = Person.from_dict({'age': 32, 'name': 'suzie'})
```

The object allows data to be modified in-place using attribute access:

```python
person.name = 'frank'

person.to_dict() # {'age': 32, 'name': 'frank'}
```

When the object is created, its entries are validated using JSONSchema to ensure that they have the correct type:

```python
Person(name='Bob', age='old')
# SchemaValidationError: Invalid specification

# myschema.Person->age, validating 'type'
# 'old' is not of type 'integer'
```

To go a step further, the generated class `Person` can be extended and fit to new purposes:  

```python

class User(Person):
    _validate_on_instantiation = False # turns off invalidation at instantiation time, requiring we check .is_valid.

    @property
    def is_adult(self):
        return self.age > 18

user = User(name="Jim", age=None) 

# check if valid
print(user.is_valid) # false
# print the validation error
print(user.validation_exception) # SchemaValidationError: None is not of type 'integer'

#another way to check validity at runtime
user.to_dict(validate=True) # raises SchemaValidationError: None is not of type 'integer'

# fixing the issue
user.age = 33

print(user.is_valid) # true


# the special Undefined type.

```

By utilizing JSONSchema
[definitions and references](https://cswr.github.io/JsonSchema/spec/definitions_references/), much more complicated nested object hierarchies are possible, and the generated classes can be subclassed in order to create domain-specific APIs for specifying data that can be serialized to and from JSON.

## Dynamic Modules

If you do not wish to write a module to disk before importing it, you can construct the
module dynamically:

```python
import schemaperfect
api = schemaperfect.SchemaModuleGenerator(schema, root_name='Person')
dynamic_module = api.import_as('dynamic_module')
```

The module returned by this method can be used directly, or you can import from it as
with any Python module.

```python
from dynamic_module import Person
person = Person(name='suzie', age=32)
person.to_dict() # {'age': 32, 'name': 'suzie'}
```

Note, however, that the module lives only in memory, so it will
only be available in the Python session in which it is defined.

## Installation

You can install the released version from [PyPI](http://pypi.python.org/pypi/schemaperfect) using ``pip``:

    $ pip install schemaperfect

To install the bleeding-edge version from source, you can download this
repository and installing locally:

    $ git clone https://github.com/jwilson8767/schemaperfect.git
    $ cd schemaperfect
    $ pip install .

## Testing

To run the test suite you must have [py.test](http://pytest.org/latest/) installed.
To run the tests, use

```
py.test --pyargs schemaperfect
```
(you can omit the `--pyargs` flag if you are running the tests from a source checkout).


## License

``schemaperfect`` is released under a [3-Clause BSD License](LICENSE).


## Feedback and Contribution

We welcome any input, feedback, bug reports, and contributions via schemaperfect's
[GitHub repository](http://github.com/jwilson8767/schemaperfect/).
