Introducing new Tools
---------------------

Here you can find details that will be helpful while introducing new type of Tools to backend. This tutorial
assumes that you know how to run MedTagger. If not, go [here](development_setup_native.md) to learn how to run it 
natively, or [here](development_in_vagrant.md) to learn how to run it in Vagrant. 

### Step 1. Add tool to the definitions

Add your new Tool to the `medtagger/definitions.py` file. The `LabelTool` enum defines all Tools supported 
by MedTagger.

### Step 2. Create tool database model

To enable support for various Label types we have introduced a concept of `LabelElement` which can be seen in 
`medtagger/database/models.py`. It provides higher level of abstraction for Label's result made with given Tool.
You can read more [here](http://docs.sqlalchemy.org/en/latest/orm/inheritance.html)

As you can see in the `LabelElement`, our `tool` column serves as the discriminator, which indicates the type
of represented object:

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

### Step 3. Preparing alembic migration

After introducing new model to our database we need to update its structure. Please refer to 
[this](changing_database_models.md) tutorial to learn how to do that.

### Step 4. Functions for adding new Label

#### Step 4.1 Repository

Create a function in `medtagger/repositories/labels.py` that will create new 'NewToolLabelElement' using
`db_session`. Please refer to other examples in the same file.

#### Step 4.2 Business

Create function in `medtagger/api/scans/business.py` that will call function you have created in the last 
step. Please refer to other examples in the same file.

Now search for `add_label_element` function in the same file. As you can see this function handles adding 
new Label Elements by the Tool that the Label was made with. Please add your tool and the method that will 
be responsible for creating such Label.

If your Tool requires some additional validation, please write the validation function and add it to 
`validate_label_payload` in `medtagger/api/scans/business.py`.

#### Step 4.3 REST Service

As you can see in `medtagger/api/scans/service_rest.py` we do already have endpoint that adds new Label for 
given scan. It is important to define a schema that will ensure that whatever JSON representation 
of a Label made with your Tool is, it is correct.

To define a schema proceed to `medtagger/api/scans/serializers.py`. As you can see, we have defined a schema 
for every `LabelElement`:

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

Below is an example of one of the schemas for Label made with Rectangle Tool:

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

Now you need to:

1. Create your own definition of the schema,
2. Write down every property that your `new_tool_label_element` should have,
3. Provide additional information about properties (type, range etc.),
4. Make sure to define which of your properties are required,
5. Add your new definition to the `oneOf` section of the `elements_schema`.

If you want more info about how to create such schemas, visit 
[this](https://json-schema.org/understanding-json-schema/index.html) page.

### Step 5. Tests

To make sure that all of this actually works, we need to write some tests! Go to the
`tests/functional_tests/test_adding_new_label.py` which contains all tests for creating Label with every Tool 
that is supported by MedTagger. As you can see all of the tests have following steps:

1. Add Scan to the system,
2. Label it with a given tool,
3. Fetch details for the label.

Add any number of tests that you think is necessary for your Tool.

Run the following command from `backend` directory to run MedTagger's functional tests:
```bash
$ make functional_tests
```

Remember to make sure that your code passes linter tests! Run the following command from the `backend` directory: 
```bash
$ make tests    
```

If you want to know more about MedTagger's tests, go [here](testing.md).

If all of your tests pass, you are all done! You have succesfully added a new Tool to MedTagger.
