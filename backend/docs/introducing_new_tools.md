Introducing new tools
------------------------------------

Here you can find every information that will be helpful with introducing new type of tools to backend. This tutorial assumes that you know how to run MedTagger. If not, go [here](development_setup_native.md) to learn how to run it natively, or [here](development_in_vagrant.md) to learn how to run it in Vagrant.

### Add tool to the enum

First step is to add your new tool to the `medtagger/definitions.py`. The `LabelTool` enum defines all tools supported by MedTagger.

### Create tool database model

To enable support for various labels types we introduced a concept of `LabelElement` which can be seen in `medtagger/database/models.py/`. It represent a high level LabelElement after which more specific types of LabelElement can inherit from. You can read more [here](http://docs.sqlalchemy.org/en/latest/orm/inheritance.html)

As you can see from the `LabelElement` our `tool` column serves as the discriminator, which indicates the type of represented object:

```python
    __mapper_args__ = {
        'polymorphic_identity': 'LabelElement',
        'polymorphic_on': tool,
    }
```

Now let's create our own model!

```python
class NewToolsLabelElement(LabelElement):
    """Definition of a Label Element made with New Tool."""

    __tablename__ = 'NewToolLabelElements'
    id: LabelElementID = Column(String, ForeignKey('LabelElements.id'), primary_key=True)

    # Here provide a set of parameters that are relevant to your NewToolLabelElement.

    __mapper_args__ = {
        'polymorphic_identity': LabelTool.NewTool,
    }

    # Your NewToolsLabelElement should also have __init__ and __repr__ methods.
```

### Performing alembic migration

After introducing new model to our database we need to update it. Please refer to [this](changing_database_models.md) tutorial to learn how to do that.

### Methods for adding new label

#### Repository

Create a method in `medtagger/repositories/labels.py` that will create a new `db_session` and add your NewToolLabelElement. Please refer to other examples in the same file.

#### Buisness

Create a method in `medtagger/api/scans/business.py` that will call your `add_new_new_tool_label_element` that we created in the last step. Please refer to other examples in the same file.

Now search for `add_label_element` method in the same file. As you can see this method handless adding new label elements by the tool that the label was made with. Please add your tool and the method that will be responsible for creating such label.

If your tool requires some additional validation. Please write the validation funtion and add it to `validate_label_payload` in `medtagger/api/scans/business.py`.

#### REST Service

As you can see in `medtagger/api/scans/service_rest.py` we do already have endpoint that add new label for given scan. What is now important to is to define a schema that will ensure that whatever JSON representation of a label made with your new tool is correct.


To define a schema proceed to `medtagger/api/scans/serializers.py`. As you can see we have defined a schema for every `LabelElement` and we are actually telling that our new `LabelElement` can be one of the following types:

```python
elements_schema = {
    'type': 'array',
    "items": {
        "type": "object",
        'oneOf': [
            {'$ref': '#/definitions/rectangular_label_element_schema'},
            {'$ref': '#/definitions/brush_label_element_schema'},
            {'$ref': '#/definitions/point_label_element_schema'},
            {'$ref': '#/definitions/chain_label_element_schema'},
        ],
    },
```
Below is and example of one of the schemas:

```python
'rectangular_label_element_schema': {
    'properties': {
        'x': {'type': 'number', 'minimum': 0.0, 'maximum': 1.0},
        'y': {'type': 'number', 'minimum': 0.0, 'maximum': 1.0},
        'width': {'type': 'number', 'minimum': 0.0, 'maximum': 1.0},
        'height': {'type': 'number', 'minimum': 0.0, 'maximum': 1.0},
        'slice_index': {'type': 'integer'},
        'tag': {'type': 'string'},
        'tool': {'type': 'string', 'pattern': 'RECTANGLE'},
    },
    'required': ['x', 'y', 'width', 'height', 'slice_index', 'tag', 'tool'],
    'additionalProperties': False,
},
```
Your job would be now to:

1. Create your own definition of the schema,
2. Write down every property that your `new_tool_label_element` should have,
3. Provide additional information about properties (type, range etc.),
4. Make sure to define which of the properties are required,
5. Add your new definition to the `oneOf` section of the `elements_schema`.

If you want more info about how to create such schemas, visit [this](https://json-schema.org/understanding-json-schema/index.html) page

### Tests

To make sure that all this actually works, we need to write some tests! Proceed to `tests/functional_tests/test_adding_new_label.py`. This file holds tests for creating label for every tool that is supported by MedTagger. As you can see all of the tests have following steps:

1. Add Scan to the system,
2. Label it with a given tool,
3. Fetch details for the label.

Add any number of tests that you think is necessary for your tool.

Run the following command from `backend` directory to run MedTagger's functional tests:
```bash
    $ make functional_tests
```

Remember to make sure that your code passes linter tests. To do the testing, please run the following command from the `backend` directory: 
```bash
    $ make tests    
```

If you want to know more about MedTagger's tests, go [here](testing.md)

If all of your tests passes you are all done! You have succesfully added a new tool to MedTagger.