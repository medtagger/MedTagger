"""Module responsible for defining all of the relational database models."""
# pylint: disable=too-few-public-methods,too-many-instance-attributes
import enum
import uuid
from typing import List, Optional

from sqlalchemy import Column, Integer, Float, String, ForeignKey, Boolean, Table, Enum, and_
from sqlalchemy.orm import relationship

from medtagger.database import Base, db_session
from medtagger.definitions import ScanStatus, SliceStatus, SliceOrientation
from medtagger.types import ScanID, SliceID, LabelID, LabelElementID, SliceLocation, SlicePosition, LabelPosition, \
    LabelShape, LabelingTime, LabelTagID

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


class UserSettings(Base):
    """Settings of user."""

    __tablename__ = 'UserSettings'
    id: int = Column(Integer, ForeignKey('Users.id'), primary_key=True)
    skip_tutorial: bool = Column(Boolean, nullable=False)

    def __init__(self) -> None:
        """Initialize UserSettings."""
        self.skip_tutorial = False


class ScanCategory(Base):
    """Definition of a Scan Category."""

    __tablename__ = 'ScanCategories'
    id: int = Column(Integer, autoincrement=True, primary_key=True)
    key: str = Column(String(50), nullable=False, unique=True)
    name: str = Column(String(100), nullable=False)
    image_path: str = Column(String(100), nullable=False)

    available_tags: List['LabelTag'] = relationship("LabelTag", back_populates="scan_category")

    def __init__(self, key: str, name: str, image_path: str) -> None:
        """Initialize Scan Category.

        :param key: unique key representing Scan Category
        :param name: name which describes this Category
        :param image_path: path to the image which is located on the frontend
        """
        self.key = key
        self.name = name
        self.image_path = image_path

    def __repr__(self) -> str:
        """Return string representation for Scan Category."""
        return '<{}: {}: {}: {}>'.format(self.__class__.__name__, self.id, self.key, self.name)


class Scan(Base):
    """Definition of a Scan."""

    __tablename__ = 'Scans'
    id: ScanID = Column(String, primary_key=True)
    status: ScanStatus = Column(Enum(ScanStatus), nullable=False, default=ScanStatus.NEW)
    declared_number_of_slices: int = Column(Integer, nullable=False)

    category_id: int = Column(Integer, ForeignKey('ScanCategories.id'))
    category: ScanCategory = relationship('ScanCategory')

    owner_id: Optional[int] = Column(Integer, ForeignKey('Users.id'))
    owner: Optional[User] = relationship('User', back_populates='scans')

    slices: List['Slice'] = relationship('Slice', back_populates='scan', order_by=lambda: Slice.location)
    labels: List['Label'] = relationship('Label', back_populates='scan')

    def __init__(self, category: ScanCategory, declared_number_of_slices: int, user: Optional[User]) -> None:
        """Initialize Scan.

        :param category: Scan's category
        :param declared_number_of_slices: number of Slices that will be uploaded later
        :param user: User that uploaded scan
        """
        self.id = ScanID(str(uuid.uuid4()))
        self.category = category
        self.declared_number_of_slices = declared_number_of_slices
        self.owner_id = user.id if user else None

    def __repr__(self) -> str:
        """Return string representation for Scan."""
        return '<{}: {}: {}: {}>'.format(self.__class__.__name__, self.id, self.category.key, self.owner)

    @property
    def width(self) -> Optional[int]:
        """Return width of a Scan/Slices in Z axis."""
        random_slice = Slice.query.filter(and_(
            Slice.scan_id == self.id,
            Slice.orientation == SliceOrientation.Z,
        )).first()
        return random_slice.width if random_slice else None

    @property
    def height(self) -> Optional[int]:
        """Return height of a Scan/Slices in Z axis."""
        random_slice = Slice.query.filter(and_(
            Slice.scan_id == self.id,
            Slice.orientation == SliceOrientation.Z,
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


class LabelVerificationStatus(enum.Enum):
    """Defines available verification status for Label."""

    VERIFIED = 'VERIFIED'
    NOT_VERIFIED = 'NOT_VERIFIED'


class Label(Base):
    """Definition of a Label."""

    __tablename__ = 'Labels'
    id: LabelID = Column(String, primary_key=True)
    scan_id: ScanID = Column(String, ForeignKey('Scans.id'))
    labeling_time: LabelingTime = Column(Float, nullable=True)

    scan: Scan = relationship('Scan', back_populates='labels')

    elements: 'LabelElement' = relationship('LabelElement', back_populates='label')

    owner_id: int = Column(Integer, ForeignKey('Users.id'))
    owner: User = relationship('User', back_populates='labels')

    status: LabelVerificationStatus = Column(Enum(LabelVerificationStatus), nullable=False,
                                             server_default=LabelVerificationStatus.NOT_VERIFIED.value)

    def __init__(self, user: User, labeling_time: LabelingTime) -> None:
        """Initialize Label.

        By default all of the labels are not verified
        """
        self.id = LabelID(str(uuid.uuid4()))
        self.owner = user
        self.labeling_time = labeling_time

    def __repr__(self) -> str:
        """Return string representation for Label."""
        return '<{}: {}: {} {} {}>'.format(self.__class__.__name__, self.id, self.scan_id,
                                           self.labeling_time, self.owner)


class LabelTag(Base):
    """Definition of tag for label."""

    __tablename__ = 'LabelTags'
    id: LabelTagID = Column(String, autoincrement=True, primary_key=True)
    key: str = Column(String(50), nullable=False, unique=True)
    name: str = Column(String(100), nullable=False)

    scan_category_id: int = Column(Integer, ForeignKey('ScanCategories.id'))
    scan_category: ScanCategory = relationship('ScanCategory', back_populates="available_tags")

    def __init__(self, key: str, name: str) -> None:
        """Initialize Label Tag.
        :param key: unique key representing Label Tag
        :param name: name which describes this Label Tag
        """
        self.key = key
        self.name = name

    def __repr__(self) -> str:
        """Return string representation for Label Tag."""
        return '<{}: {}: {}: {}>'.format(self.__class__.__name__, self.id, self.key, self.name)


class LabelElementStatus(enum.Enum):
    """Defines available status for Label Element."""

    VALID = 'VALID'
    INVALID = 'INVALID'
    NOT_VERIFIED = 'NOT_VERIFIED'


class LabelElement(Base):
    """Definition of a Label Element."""

    __tablename__ = 'LabelElements'
    id: LabelElementID = Column(String, primary_key=True)
    position_x: float = Column(Float, nullable=False)
    position_y: float = Column(Float, nullable=False)
    slice_index: int = Column(Integer, nullable=False)
    shape_width: float = Column(Float, nullable=False)
    shape_height: float = Column(Float, nullable=False)
    has_binary_mask: bool = Column(Boolean, nullable=False)

    label_id: LabelID = Column(String, ForeignKey('Labels.id'))
    label: Label = relationship('Label', back_populates='selections')

    tag_id: LabelTagID = Column(String, ForeignKey('LabelTags.id'))
    tag: 'LabelTag' = relationship('LabelTag', back_populates="label_element")

    status: LabelElementStatus = Column(Enum(LabelElementStatus), nullable=False,
                                        server_default=LabelElementStatus.NOT_VERIFIED.value)

    def __init__(self, position: LabelPosition, shape: LabelShape, label_tag: LabelTag,
                 has_binary_mask: bool = False) -> None:
        """Initialize Label Element.

        :param position: position (x, y, slice_index) of the label
        :param shape: shape (width, height) of the label
        :param label_tag: tag of the label
        :param has_binary_mask: boolean information if such Label Element has binary mask or not
        """
        self.id = LabelElementID(str(uuid.uuid4()))
        self.position_x = position.x
        self.position_y = position.y
        self.slice_index = position.slice_index
        self.shape_width = shape.width
        self.shape_height = shape.height
        self.label_tag = label_tag
        self.has_binary_mask = has_binary_mask
        self.status = LabelElementStatus.NOT_VERIFIED

    def __repr__(self) -> str:
        """Return string representation for Label Element."""
        _has_binary_mask = 'WITH BINARY MASK' if self.has_binary_mask else 'WITHOUT BINARY MASK'
        return '<{}: {}: {}>'.format(self.__class__.__name__, self.id, _has_binary_mask)

    def update_status(self, status: LabelElementStatus) -> 'LabelElement':
        """Update Label's element status.

        :param status: new status for this Label Element
        :return: Label Element object
        """
        self.status = status
        self.save()
        return self
