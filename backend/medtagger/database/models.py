"""Module responsible for defining all of the relational database models."""
# pylint: disable=too-few-public-methods,too-many-instance-attributes
import uuid
from typing import List, Dict, cast, Optional, Any

from sqlalchemy import Column, Integer, Float, String, ForeignKey, Boolean, Enum, Table, and_
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from medtagger.database.utils import ArrayOfEnum
from medtagger.database import Base, db_session
from medtagger.definitions import ScanStatus, SliceStatus, SliceOrientation, LabelVerificationStatus, \
    LabelElementStatus, LabelTool
from medtagger.types import ScanID, SliceID, LabelID, LabelElementID, SliceLocation, SlicePosition, \
    LabelPosition, LabelShape, LabelingTime, LabelTagID, ActionID, SurveyID, SurveyElementID, SurveyElementKey, \
    ActionResponseID, SurveyResponseID, PointID, TaskID

#########################
#
#  Users related models
#
#########################

users_roles = Table('Users_Roles', Base.metadata,
                    Column('user_id', Integer, ForeignKey('Users.id')),
                    Column('role_id', Integer, ForeignKey('Roles.id')))


class Role(Base):
    """Defines model for the Roles table."""

    __tablename__ = 'Roles'
    id: int = Column(Integer, autoincrement=True, primary_key=True)
    name: str = Column(String(50), unique=True)

    def __init__(self, name: str) -> None:
        """Initialize Role."""
        self.name = name


class User(Base):
    """Defines model for the Users table."""

    __tablename__ = 'Users'
    id: int = Column(Integer, autoincrement=True, primary_key=True)
    email: str = Column(String(50), nullable=False, unique=True)
    password: str = Column(String(255), nullable=False)
    first_name: str = Column(String(50), nullable=False)
    last_name: str = Column(String(50), nullable=False)
    active: bool = Column(Boolean, nullable=False)

    roles: List[Role] = relationship('Role', secondary=users_roles)
    settings = relationship('UserSettings', uselist=False)
    scans: List['Scan'] = relationship('Scan', back_populates='owner')
    labels: List['Label'] = relationship('Label', back_populates='owner')

    def __init__(self, email: str, password_hash: str, first_name: str, last_name: str) -> None:
        """Initialize User."""
        self.email = email
        self.password = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.active = False
        self.settings = UserSettings()

    def __repr__(self) -> str:
        """Return string representation for User."""
        return '<{}: {}: {}>'.format(self.__class__.__name__, self.id, self.email)

    @property
    def role(self) -> Role:
        """Return role for User."""
        return self.roles[0]


#########################
#
#  Scans related models
#
#########################

class UserSettings(Base):
    """Settings of user."""

    __tablename__ = 'UserSettings'
    id: int = Column(Integer, ForeignKey('Users.id'), primary_key=True)
    skip_tutorial: bool = Column(Boolean, nullable=False)

    def __init__(self) -> None:
        """Initialize UserSettings."""
        self.skip_tutorial = False


datasets_tasks = Table('Datasets_Tasks', Base.metadata,
                       Column('dataset_id', Integer, ForeignKey('Datasets.id'), nullable=False),
                       Column('task_id', Integer, ForeignKey('Tasks.id'), nullable=False))


class Dataset(Base):
    """Definition of a Dataset."""

    __tablename__ = 'Datasets'
    id: int = Column(Integer, autoincrement=True, primary_key=True)
    key: str = Column(String(50), nullable=False, unique=True)
    name: str = Column(String(100), nullable=False)
    disabled: bool = Column(Boolean, nullable=False, server_default='f')

    tasks: List['Task'] = relationship('Task', back_populates='datasets', secondary=datasets_tasks)

    def __init__(self, key: str, name: str) -> None:
        """Initialize Dataset.

        :param key: unique key representing Dataset
        :param name: name which describes this Dataset
        """
        self.key = key
        self.name = name

    def __repr__(self) -> str:
        """Return string representation for Dataset."""
        return '<{}: {}: {}: {}>'.format(self.__class__.__name__, self.id, self.key, self.name)


class Task(Base):
    """Describe what user should mark on Scans in given Datasets."""

    __tablename__ = 'Tasks'
    id: TaskID = Column(Integer, autoincrement=True, primary_key=True)
    key: str = Column(String(50), nullable=False, unique=True)
    name: str = Column(String(100), nullable=False)
    image_path: str = Column(String(100), nullable=False)
    disabled: bool = Column(Boolean, nullable=False, server_default='f')

    datasets: List[Dataset] = relationship('Dataset', back_populates='tasks',
                                           secondary=datasets_tasks)

    _tags: List['LabelTag'] = relationship("LabelTag", back_populates="task")

    def __init__(self, key: str, name: str, image_path: str) -> None:
        """Initialize Task.

        :param key: unique key representing Task
        :param name: name which describes this Task
        :param image_path: path to the image which is located on the frontend
        """
        self.key = key
        self.name = name
        self.image_path = image_path

    def __repr__(self) -> str:
        """Return string representation for Task."""
        return '<{}: {}: {}: {}>'.format(self.__class__.__name__, self.id, self.key, self.name)

    @property
    def available_tags(self) -> List['LabelTag']:
        """Return Tags that are enabled for this Task."""
        return [tag for tag in self._tags if not tag.disabled]

    @available_tags.setter
    def available_tags(self, new_tags: List['LabelTag']) -> None:
        """Set new Label Tags for this Task."""
        self._tags = new_tags


class Scan(Base):
    """Definition of a Scan."""

    __tablename__ = 'Scans'
    id: ScanID = Column(String, primary_key=True)
    status: ScanStatus = Column(Enum(ScanStatus), nullable=False, default=ScanStatus.NEW)
    declared_number_of_slices: int = Column(Integer, nullable=False)
    skip_count: int = Column(Integer, nullable=False, default=0)

    dataset_id: int = Column(Integer, ForeignKey('Datasets.id'))
    dataset: Dataset = relationship('Dataset')

    owner_id: Optional[int] = Column(Integer, ForeignKey('Users.id'))
    owner: Optional[User] = relationship('User', back_populates='scans')

    slices: List['Slice'] = relationship('Slice', back_populates='scan', cascade='delete', order_by=lambda: Slice.location)
    labels: List['Label'] = relationship('Label', back_populates='scan', cascade='delete')

    def __init__(self, dataset: Dataset, declared_number_of_slices: int, user: Optional[User]) -> None:
        """Initialize Scan.

        :param dataset: Dataset
        :param declared_number_of_slices: number of Slices that will be uploaded later
        :param user: User that uploaded scan
        """
        self.id = ScanID(str(uuid.uuid4()))
        self.dataset = dataset
        self.declared_number_of_slices = declared_number_of_slices
        self.owner_id = user.id if user else None

    def __repr__(self) -> str:
        """Return string representation for Scan."""
        return '<{}: {}: {}: {}>'.format(self.__class__.__name__, self.id, self.dataset.key, self.owner)

    @property
    def width(self) -> Optional[int]:
        """Return width of a Scan/Slices in Z axis."""
        random_slice = Slice.query.filter(and_(
            Slice.scan_id == self.id,
            Slice.orientation == SliceOrientation.Z,
            Slice.width.isnot(None),  # type: ignore  # "int" has no attribute "isnot"
        )).first()
        return random_slice.width if random_slice else None

    @property
    def height(self) -> Optional[int]:
        """Return height of a Scan/Slices in Z axis."""
        random_slice = Slice.query.filter(and_(
            Slice.scan_id == self.id,
            Slice.orientation == SliceOrientation.Z,
            Slice.height.isnot(None),  # type: ignore  # "int" has no attribute "isnot"
        )).first()
        return random_slice.height if random_slice else None

    def add_slice(self, orientation: SliceOrientation = SliceOrientation.Z) -> 'Slice':
        """Add new slice into this Scan.

        :return: ID of a Slice
        """
        with db_session() as session:
            new_slice = Slice(orientation)
            new_slice.scan = self
            session.add(new_slice)
        return new_slice

    def update_status(self, status: ScanStatus) -> 'Scan':
        """Update Scan's status.

        :param status: new status for this Scan
        :return: Scan object
        """
        self.status = status
        self.save()
        return self


class Slice(Base):
    """Definition of a Slice."""

    __tablename__ = 'Slices'
    id: SliceID = Column(String, primary_key=True)
    status: SliceStatus = Column(Enum(SliceStatus), nullable=False, default=SliceStatus.NEW)
    orientation: SliceOrientation = Column(Enum(SliceOrientation), nullable=False, default=SliceOrientation.Z)
    location: float = Column(Float, nullable=True)
    position_x: float = Column(Float, nullable=True)
    position_y: float = Column(Float, nullable=True)
    position_z: float = Column(Float, nullable=True)
    width: int = Column(Integer, nullable=True)
    height: int = Column(Integer, nullable=True)

    scan_id: ScanID = Column(String, ForeignKey('Scans.id'))
    scan: Scan = relationship('Scan', back_populates='slices')

    def __init__(self, orientation: SliceOrientation, location: SliceLocation = None,
                 position: SlicePosition = None) -> None:
        """Initialize Slice.

        :param orientation: orientation of the Slice
        :param location: location of a Slice (useful for sorting)
        :param position: position of a Slice inside of a patient body
        """
        self.id = SliceID(str(uuid.uuid4()))
        self.orientation = orientation
        if location:
            self.location = location
        if position:
            self.position_x = position.x
            self.position_y = position.y
            self.position_z = position.z

    def __repr__(self) -> str:
        """Return string representation for Slice."""
        return '<{}: {}: {}: {}>'.format(self.__class__.__name__, self.id, self.location, self.orientation)

    def update_location(self, new_location: SliceLocation) -> 'Slice':
        """Update location in the Slice."""
        self.location = new_location
        self.save()
        return self

    def update_position(self, new_position: SlicePosition) -> 'Slice':
        """Update position in the Slice."""
        self.position_x = new_position.x
        self.position_y = new_position.y
        self.position_z = new_position.z
        self.save()
        return self

    def update_size(self, height: int, width: int) -> 'Slice':
        """Update height & width in the Slice."""
        self.height = height
        self.width = width
        self.save()
        return self

    def update_status(self, status: SliceStatus) -> 'Slice':
        """Update Slice's status.

        :param status: new status for this Slice
        :return: Slice object
        """
        self.status = status
        self.save()
        return self


##########################
#
#  Labels related models
#
##########################

class Label(Base):
    """Definition of a Label."""

    __tablename__ = 'Labels'
    id: LabelID = Column(String, primary_key=True)
    scan_id: ScanID = Column(String, ForeignKey('Scans.id'))
    scan: Scan = relationship('Scan', back_populates='labels')
    task_id: TaskID = Column(Integer, ForeignKey('Tasks.id'), nullable=False)
    task: Task = relationship('Task')

    labeling_time: LabelingTime = Column(Float, nullable=True)

    elements: List['LabelElement'] = relationship('LabelElement', back_populates='label', cascade='delete')

    owner_id: int = Column(Integer, ForeignKey('Users.id'))
    owner: User = relationship('User', back_populates='labels')

    status: LabelVerificationStatus = Column(Enum(LabelVerificationStatus), nullable=False,
                                             server_default=LabelVerificationStatus.NOT_VERIFIED.value)

    comment: Optional[str] = Column(String, nullable=True)

    def __init__(self, user: User, labeling_time: LabelingTime, comment: str = None) -> None:
        """Initialize Label.

        By default all of the labels are not verified
        """
        self.id = LabelID(str(uuid.uuid4()))
        self.owner = user
        self.labeling_time = labeling_time
        self.status = LabelVerificationStatus.NOT_VERIFIED
        self.comment = comment

    def __repr__(self) -> str:
        """Return string representation for Label."""
        return '<{}: {}: {}: {} {} {} {}>'.format(self.__class__.__name__, self.id, self.scan_id, self.task_id,
                                                  self.labeling_time, self.owner, self.comment)

    def update_status(self, status: LabelVerificationStatus) -> 'Label':
        """Update Label's verification status.

        :param status: new status for this Label
        :return: Label object
        """
        self.status = status
        self.save()
        return self


class LabelTag(Base):
    """Definition of tag for label."""

    __tablename__ = 'LabelTags'
    id: LabelTagID = Column(Integer, autoincrement=True, primary_key=True)
    key: str = Column(String(50), nullable=False, unique=True)
    name: str = Column(String(100), nullable=False)
    disabled: bool = Column(Boolean, nullable=False, server_default='f')

    task_id: TaskID = Column(Integer, ForeignKey('Tasks.id'), nullable=False)
    task: Task = relationship('Task', back_populates="_tags")

    tools: List[LabelTool] = Column(ArrayOfEnum(Enum(LabelTool, name='label_tool', create_constraint=False)))
    actions: List['Action'] = relationship('Action', back_populates='label_tag')

    def __init__(self, key: str, name: str, tools: List[LabelTool], actions: List['Action'] = None) -> None:
        """Initialize Label Tag.

        :param key: unique key representing Label Tag
        :param name: name which describes this Label Tag
        :param tools: list of tools for given Label Tag that will be available on labeling page
        :param actions: (optional) list of required actions for this Label Tag
        """
        self.key = key
        self.name = name
        self.tools = tools
        self.actions = actions or []

    def __repr__(self) -> str:
        """Return string representation for Label Tag."""
        return '<{}: {}: {}: {}>'.format(self.__class__.__name__, self.id, self.key, self.name)


class LabelElement(Base):
    """Definition of high level Label Element."""

    __tablename__ = 'LabelElements'
    id: LabelElementID = Column(String, primary_key=True)

    slice_index: int = Column(Integer, nullable=False)

    label_id: LabelID = Column(String, ForeignKey('Labels.id'))
    label: Label = relationship('Label', back_populates='elements')

    tag_id: LabelTagID = Column(Integer, ForeignKey('LabelTags.id'))
    tag: LabelTag = relationship('LabelTag')

    status: LabelElementStatus = Column(Enum(LabelElementStatus), nullable=False,
                                        server_default=LabelElementStatus.NOT_VERIFIED.value)

    tool: LabelTool = Column(Enum(LabelTool), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'LabelElement',
        'polymorphic_on': tool,
    }

    def __init__(self, tag: LabelTag) -> None:
        """Initialize Label Element.

        :param tag: tag of the label
        """
        self.id = LabelElementID(str(uuid.uuid4()))
        self.tag_id = tag.id
        self.status = LabelElementStatus.NOT_VERIFIED

    def __repr__(self) -> str:
        """Return string representation for Label Element."""
        return '<{}: {}>'.format(self.__class__.__name__, self.id)

    def update_status(self, status: LabelElementStatus) -> 'LabelElement':
        """Update Label's element status.

        :param status: new status for this Label Element
        :return: Label Element object
        """
        self.status = status
        self.save()
        return self


class RectangularLabelElement(LabelElement):
    """Definition of a Label Element made with Rectangle Tool."""

    __tablename__ = 'RectangularLabelElements'
    id: LabelElementID = Column(String, ForeignKey('LabelElements.id'), primary_key=True)

    x: float = Column(Float, nullable=False)
    y: float = Column(Float, nullable=False)
    width: float = Column(Float, nullable=False)
    height: float = Column(Float, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': LabelTool.RECTANGLE,
    }

    def __init__(self, position: LabelPosition, shape: LabelShape, tag: LabelTag) -> None:
        """Initialize LabelElement.

        :param position: position (x, y, slice_index) of the label
        :param shape: shape (width, height) of the label
        :param tag: tag of the label
        """
        super(RectangularLabelElement, self).__init__(tag)
        self.x = position.x
        self.y = position.y
        self.slice_index = position.slice_index
        self.width = shape.width
        self.height = shape.height

    def __repr__(self) -> str:
        """Return string representation for  Rectangular Label Element."""
        return '<{}: {}>'.format(self.__class__.__name__, self.id)


class BrushLabelElement(LabelElement):
    """Definition of a Label Element made with Brush Tool."""

    __tablename__ = 'BrushLabelElements'
    id: LabelElementID = Column(String, ForeignKey('LabelElements.id'), primary_key=True)

    width: int = Column(Integer, nullable=False)
    height: int = Column(Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': LabelTool.BRUSH,
    }

    def __init__(self, slice_index: int, width: int, height: int, tag: LabelTag) -> None:
        """Initialize LabelElement made with Brush Tool.

        :param slice_index: integer value representing index of a Slice in asc order
        :param width: width of the label's image
        :param height: height of the label's image
        :param tag: tag of the label
        """
        super(BrushLabelElement, self).__init__(tag)
        self.slice_index = slice_index
        self.width = width
        self.height = height

    def __repr__(self) -> str:
        """Return string representation for Brush Label Element."""
        return '<{}: {}>'.format(self.__class__.__name__, self.id)


class PointLabelElement(LabelElement):
    """Definition of a Label Element made with Point Tool."""

    __tablename__ = 'PointLabelElements'
    id: LabelElementID = Column(String, ForeignKey('LabelElements.id'), primary_key=True)

    x: float = Column(Float, nullable=False)
    y: float = Column(Float, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': LabelTool.POINT,
    }

    def __init__(self, position: LabelPosition, tag: LabelTag) -> None:
        """Initialize LabelElement made with Point Tool.

        :param position: position (x, y, slice_index) of the label
        :param tag: tag of the label
        """
        super().__init__(tag)
        self.slice_index = position.slice_index
        self.x = position.x
        self.y = position.y

    def __repr__(self) -> str:
        """Return string representation for Point Label Element."""
        return '<{}: {}>'.format(self.__class__.__name__, self.id)


class ChainLabelElement(LabelElement):
    """Definition of a Label Element made with Chain Tool."""

    __tablename__ = 'ChainLabelElements'
    id: LabelElementID = Column(String, ForeignKey('LabelElements.id'), primary_key=True)

    points: List['ChainLabelElementPoint'] = relationship('ChainLabelElementPoint',
                                                          order_by='ChainLabelElementPoint.order',
                                                          back_populates='label_element')
    loop: bool = Column(Boolean, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': LabelTool.CHAIN,
    }

    def __init__(self, slice_index: int, tag: LabelTag, loop: bool) -> None:
        """Initialize LabelElement made with Point Tool.

        :param slice_index: index of slice
        :param tag: tag of the label
        :param loop: true if chain is loop (first and last points are connected)
        """
        super().__init__(tag)
        self.slice_index = slice_index
        self.loop = loop

    def __repr__(self) -> str:
        """Return string representation for Chain Label Element."""
        return '<{}: {}: {} {}>'.format(self.__class__.__name__, self.id, len(self.points), self.loop)


class ChainLabelElementPoint(Base):
    """Definition of one point in a chain created by Chain Tool."""

    __tablename__ = 'ChainLabelElementPoints'
    id: PointID = Column(String, primary_key=True)

    x: float = Column(Float, nullable=False)
    y: float = Column(Float, nullable=False)
    label_element_id: LabelElementID = Column(String, ForeignKey('LabelElements.id'), nullable=False)
    label_element: ChainLabelElement = relationship('ChainLabelElement', back_populates='points')
    order: int = Column(Integer, nullable=False)

    def __init__(self, x: float, y: float, label_element_id: LabelElementID, order: int) -> None:
        """Initialize Point made with Chain Tool.

        :param x: position x of point
        :param y: position y of point
        :param label_element_id: id of ChainLabelElement that point belongs to
        :param order: 0-indexed position of point in chain, points with consecutive order numbers are connected,
                      points with order 0 and last order are connected if chain is loop
        """
        self.id = PointID(str(uuid.uuid4()))
        self.x = x
        self.y = y
        self.label_element_id = label_element_id
        self.order = order

    def __repr__(self) -> str:
        """Return string representation for Chain Label Element Point."""
        return '<{}: {}: {} {}>'.format(self.__class__.__name__, self.id, self.x, self.y)


###########################
#
#  Actions related models
#
###########################

class Action(Base):
    """Definition of a high level Action."""

    __tablename__ = 'Actions'
    id: ActionID = Column(Integer, autoincrement=True, primary_key=True)
    name: str = Column(String(255), nullable=False)
    action_type: str = Column(String(50), nullable=False)

    label_tag_id: int = Column(Integer, ForeignKey('LabelTags.id'))
    label_tag: LabelTag = relationship('LabelTag', back_populates='actions')

    responses: List['ActionResponse'] = relationship('ActionResponse', back_populates='action')

    __mapper_args__ = {
        'polymorphic_identity': 'Action',
        'polymorphic_on': action_type,
    }

    def __init__(self, name: str) -> None:
        """Initialize Action.

        :param name: name that should identify such actions for given Dataset
        """
        self.name = name

    def __repr__(self) -> str:
        """Return string representation for Action."""
        return '<{}: {}: "{}">'.format(self.__class__.__name__, self.id, self.name)


class Survey(Action):
    """Definition of a Survey."""

    __tablename__ = 'Surveys'
    id: SurveyID = Column(Integer, ForeignKey('Actions.id'), primary_key=True)
    initial_element_key: SurveyElementKey = Column(String(50), nullable=False)

    elements: List['SurveyElement'] = relationship('SurveyElement', back_populates='survey')
    responses: List['SurveyResponse'] = relationship('SurveyResponse', back_populates='survey')

    __mapper_args__ = {
        'polymorphic_identity': 'Survey',
    }

    def __init__(self, name: str, initial_element_key: SurveyElementKey) -> None:
        """Initialize Action.

        :param name: name that should identify such actions for given Dataset
        :param initial_element_key: key for an element that is initial for whole Survey
        """
        super(Survey, self).__init__(name)
        self.initial_element_key = initial_element_key

    def get_details(self) -> Dict:
        """Return dictionary details about this Survey."""
        return {
            'name': self.name,
            'initial_element_key': self.initial_element_key,
            'elements': [element.get_details() for element in self.elements],
        }

    def validate_response(self, response: Dict) -> bool:
        """Validate incoming Response for this Survey."""
        elements_keys = {element.key for element in self.elements}
        response_keys = set(response)
        return response_keys.issubset(elements_keys)


class SurveyElement(Base):
    """Definition of a single element in Survey."""

    __tablename__ = 'SurveyElements'
    id: SurveyElementID = Column(Integer, autoincrement=True, primary_key=True)
    key: SurveyElementKey = Column(String(50), nullable=False)
    instant_next_element: Optional[SurveyElementKey] = Column(String(50), nullable=True)
    survey_element_type: str = Column(String(50), nullable=False)

    survey_id: SurveyID = Column(Integer, ForeignKey('Surveys.id'))
    survey: Survey = relationship('Survey', back_populates='elements')

    __mapper_args__ = {
        'polymorphic_identity': 'SurveyElement',
        'polymorphic_on': survey_element_type,
    }

    def __init__(self, key: SurveyElementKey, instant_next_element: Optional[SurveyElementKey] = None) -> None:
        """Initialize an element in Survey.

        :param key: key that will identify this Element in whole Survey
        :param instant_next_element: key for next Survey Element that should show instantaneously
        """
        self.key = key
        self.instant_next_element = instant_next_element

    def get_details(self) -> Dict:
        """Return dictionary details about this Element from Survey."""
        return {
            'key': self.key,
            'instant_next_element': self.instant_next_element,
            'type': self.survey_element_type,
        }


class SurveySingleChoiceQuestion(SurveyElement):
    """Definition of a Single Choise Question in Survey."""

    __tablename__ = 'SurveySingleChoiceQuestions'
    id: SurveyElementID = Column(Integer, ForeignKey('SurveyElements.id'), primary_key=True)
    title: str = Column(String(255), nullable=False)
    possible_answers: Dict[str, Optional[SurveyElementKey]] = Column(JSONB, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'SurveySingleChoiceQuestion',
    }

    def __init__(self, key: SurveyElementKey, title: str, possible_answers: Dict[str, Optional[SurveyElementKey]],
                 instant_next_element: SurveyElementKey = None) -> None:
        """Initialize a Single Choice Question in Survey.

        :param key: key that will identify this Question in whole Survey
        :param title: title for this question
        :param possible_answers: dictionary of possible answers and their next elements in Survey
        :param instant_next_element: key for next Survey Element that should show instantaneously
        """
        super(SurveySingleChoiceQuestion, self).__init__(key, instant_next_element)
        self.title = title
        self.possible_answers = possible_answers

    def __repr__(self) -> str:
        """Return string representation for SurveySingleChoiceQuestion."""
        return '<{}: {}: "{}">'.format(self.__class__.__name__, self.id, self.title)

    def get_details(self) -> Dict:
        """Return dictionary details about this Question."""
        details = super(SurveySingleChoiceQuestion, self).get_details()
        details.update({
            'title': self.title,
            'possible_answers': self.possible_answers,
        })
        return details


class ActionResponse(Base):
    """Definition of a Response for Action."""

    __tablename__ = 'ActionResponses'
    id: ActionResponseID = Column(Integer, autoincrement=True, primary_key=True)
    action_response_type: str = Column(String(50), nullable=False)

    action_id: ActionID = Column(Integer, ForeignKey('Actions.id'))
    action: Action = relationship('Action', back_populates='responses')

    __mapper_args__ = {
        'polymorphic_identity': 'ActionResponse',
        'polymorphic_on': action_response_type,
    }

    def get_details(self) -> Dict:  # pylint: disable=no-self-use
        """Return dictionary details about this Action Response."""
        return {}


class SurveyResponse(ActionResponse):
    """Definition of a Response for Survey."""

    __tablename__ = 'SurveyResponses'
    id: SurveyResponseID = Column(Integer, ForeignKey('ActionResponses.id'), primary_key=True)
    data: Dict[SurveyElementKey, Any] = Column(JSONB, nullable=False)

    survey: Survey = relationship('Survey', back_populates='responses', foreign_keys=ActionResponse.action_id)

    label_element_id: LabelElementID = Column(String, ForeignKey('LabelElements.id'))
    label_element: LabelElement = relationship('LabelElement')

    __mapper_args__ = {
        'polymorphic_identity': 'SurveyResponse',
    }

    def __init__(self, survey_id: SurveyID, data: Dict[SurveyElementKey, Any]) -> None:
        """Initialize Response for a given Survey.

        :param survey_id: ID of a Survey with which this Response is connected with
        :param data: dictionary representation of all answers where key is a Survey Element Key
        """
        super(SurveyResponse, self).__init__()
        self.action_id = cast(ActionID, survey_id)
        self.data = data

    def get_details(self) -> Dict:
        """Return dictionary details about this Survey Response."""
        return self.data
