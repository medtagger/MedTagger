Introducing new tools
------------------------------------

Here you can find every information that will be helpful with introducing new type of tools to backend.

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

Create a method in `medtagger/repositories/labels.py` that will create  a new `db_session` and add your NewToolLabelElement. Please refer to other examples in the same file.

#### Buisness

Create a method in `medtagger/api/scans/business.py` that will call your `add_new_new_tool_label_element` that we created in the last step.

Now search for `add_label_element` method in the same file. As you can see this method handless adding new label elements by the tool that the label was made with. Please add your tool and the method that will be responsible for creating such label.

#### Service

As you can see in `medtagger/api/scans/service_rest.py` we do already have endpoint that add new label for given scan. What is now important to is to make sure our `NewToolsLabelsElement` 


