"""Module responsible for defining all of the relational database models."""
# pylint: disable=too-few-public-methods,too-many-instance-attributes
import enum
import uuid
from typing import List, cast, Optional

from flask_security import UserMixin, RoleMixin
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship

from medtagger.database import Base, db_session, db
from medtagger.types import ScanID, SliceID, LabelID, LabelSelectionID, SliceLocation, SlicePosition, \
    LabelPosition, LabelShape, LabelingTime

users_roles = db.Table('Users_Roles', Base.metadata,
                       Column('user_id', Integer, ForeignKey('Users.id')),
                       Column('role_id', Integer, ForeignKey('Roles.id')))


class Role(Base, RoleMixin):
    """Defines model for the Roles table."""

    __tablename__ = 'Roles'
    id: int = Column(Integer, autoincrement=True, primary_key=True)
    name: str = Column(String(50), unique=True)

    def __init__(self, name: str) -> None:
        """Initialize Role."""
        self.name = name


class User(Base, UserMixin):
    """Defines model for the Users table."""

    __tablename__ = 'Users'
    id: int = Column(Integer, autoincrement=True, primary_key=True)
    email: str = Column(String(50), nullable=False, unique=True)
    password: str = Column(String(255), nullable=False)
    first_name: str = Column(String(50), nullable=False)
    last_name: str = Column(String(50), nullable=False)
    active: bool = Column(Boolean, nullable=False)

    roles: List[Role] = db.relationship('Role', secondary=users_roles)

    scans: List['Scan'] = relationship('Scan', back_populates='owner')
    labels: List['Label'] = relationship('Label', back_populates='owner')

    def __init__(self, email: str, password_hash: str, first_name: str, last_name: str) -> None:
        """Initialize User."""
        self.email = email
        self.password = password_hash
        self.first_name = first_name
        self.last_name = last_name
        self.active = False

    def __repr__(self) -> str:
        """Return string representation for User."""
        return '<{}: {}: {}>'.format(self.__class__.__name__, self.id, self.email)

    @property
    def role(self) -> Role:
        """Return role for User."""
        return self.roles[0]


class ScanCategory(Base):
    """Definition of a Scan Category."""

    __tablename__ = 'ScanCategories'
    id: int = Column(Integer, autoincrement=True, primary_key=True)
    key: str = Column(String(50), nullable=False, unique=True)
    name: str = Column(String(100), nullable=False)
    image_path: str = Column(String(100), nullable=False)

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


class SliceOrientation(enum.Enum):
    """Defines available Slice orientation."""

    X = 'X'
    Y = 'Y'
    Z = 'Z'


class Scan(Base):
    """Definition of a Scan."""

    __tablename__ = 'Scans'
    id: ScanID = Column(String, primary_key=True)
    converted: bool = Column(Boolean, default=False)
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
    def stored_slices(self) -> List['Slice']:
        """Return all Slices which were already stored."""
        _slice_stored_column = cast(Boolean, Slice.stored)  # MyPy understands stored as 'bool' type
        with db_session() as session:
            query = session.query(Slice)
            query = query.filter(Slice.scan_id == self.id)
            query = query.filter(_slice_stored_column.is_(True))
            return query.all()

    def add_slice(self, orientation: SliceOrientation = SliceOrientation.Z) -> 'Slice':
        """Add new slice into this Scan.

        :return: ID of a Slice
        """
        with db_session() as session:
            new_slice = Slice(orientation)
            new_slice.scan = self
            session.add(new_slice)
        return new_slice

    def mark_as_converted(self) -> 'Scan':
        """Mark Scan as 3D converted."""
        self.converted = True
        self.save()
        return self


class Slice(Base):
    """Definition of a Slice."""

    __tablename__ = 'Slices'
    id: SliceID = Column(String, primary_key=True)
    orientation: SliceOrientation = Column(Enum(SliceOrientation), nullable=False, default=SliceOrientation.Z)
    location: float = Column(Float, nullable=True)
    position_x: float = Column(Float, nullable=True)
    position_y: float = Column(Float, nullable=True)
    position_z: float = Column(Float, nullable=True)
    stored: bool = Column(Boolean, default=False)
    converted: bool = Column(Boolean, default=False)

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

    def mark_as_stored(self) -> 'Slice':
        """Mark Slice as stored in HBase."""
        self.stored = True
        self.save()
        return self

    def mark_as_converted(self) -> 'Slice':
        """Mark Slice as converted in HBase."""
        self.converted = True
        self.save()
        return self


class LabelStatus(enum.Enum):
    """Defines available status for label."""

    VALID = 'VALID'
    INVALID = 'INVALID'
    NOT_VERIFIED = 'NOT_VERIFIED'


class Label(Base):
    """Definition of a Label."""

    __tablename__ = 'Labels'
    id: LabelID = Column(String, primary_key=True)
    scan_id: ScanID = Column(String, ForeignKey('Scans.id'))
    labeling_time: LabelingTime = Column(Float, nullable=True)
    status: LabelStatus = Column(Enum(LabelStatus), nullable=False, server_default=LabelStatus.NOT_VERIFIED.value)

    scan: Scan = relationship('Scan', back_populates='labels')
    selections: 'LabelSelection' = relationship('LabelSelection', back_populates='label')

    owner_id: int = Column(Integer, ForeignKey('Users.id'))
    owner: User = relationship('User', back_populates='labels')

    def __init__(self, user: User, labeling_time: LabelingTime) -> None:
        """Initialize Label.

        By default all of the labels are not verified
        """
        self.id = LabelID(str(uuid.uuid4()))
        self.status = LabelStatus.NOT_VERIFIED
        self.owner = user
        self.labeling_time = labeling_time

    def __repr__(self) -> str:
        """Return string representation for Label."""
        return '<{}: {}: {} {} {} {}>'.format(self.__class__.__name__, self.id, self.scan_id, self.status,
                                              self.labeling_time, self.owner)

    def update_status(self, status: LabelStatus) -> 'Label':
        """Update Label's status.

        :param status: new status for this Label
        :return: Label object
        """
        self.status = status
        self.save()
        return self


class LabelSelection(Base):
    """Definition of a selection for Label."""

    __tablename__ = 'LabelSelections'
    id: LabelSelectionID = Column(String, primary_key=True)
    position_x: float = Column(Float, nullable=False)
    position_y: float = Column(Float, nullable=False)
    slice_index: int = Column(Integer, nullable=False)
    shape_width: float = Column(Float, nullable=False)
    shape_height: float = Column(Float, nullable=False)
    has_binary_mask: bool = Column(Boolean, nullable=False)

    label_id: LabelID = Column(String, ForeignKey('Labels.id'))
    label: Label = relationship('Label', back_populates='selections')

    def __init__(self, position: LabelPosition, shape: LabelShape, has_binary_mask: bool = False) -> None:
        """Initialize Label Selection.

        :param position: position (x, y, slice_index) of the label
        :param shape: shape (width, height) of the label
        :param has_binary_mask: boolean information if such Label Selection has binary mask or not
        """
        self.id = LabelSelectionID(str(uuid.uuid4()))
        self.position_x = position.x
        self.position_y = position.y
        self.slice_index = position.slice_index
        self.shape_width = shape.width
        self.shape_height = shape.height
        self.has_binary_mask = has_binary_mask

    def __repr__(self) -> str:
        """Return string representation for Label Selection."""
        _has_binary_mask = 'WITH BINARY MASK' if self.has_binary_mask else 'WITHOUT BINARY MASK'
        return '<{}: {}: {}>'.format(self.__class__.__name__, self.id, _has_binary_mask)
