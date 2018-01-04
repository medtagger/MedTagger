"""Module responsible for defining all of the relational database models."""
# pylint: disable=too-few-public-methods,too-many-instance-attributes
import enum
import uuid
from typing import List

from flask_security import UserMixin, RoleMixin
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship

from medtagger.database import Base, db_session, db
from medtagger.types import ScanID, SliceID, LabelID, LabelSelectionID, SliceLocation, SlicePosition, \
    LabelPosition, LabelShape


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
    roles = db.relationship('Role', secondary=users_roles)
    active = Column(Boolean, nullable=False)

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


class Scan(Base):
    """Definition of a Scan."""

    __tablename__ = 'Scans'
    id: ScanID = Column(String, primary_key=True)

    category_id: int = Column(Integer, ForeignKey('ScanCategories.id'))
    category: ScanCategory = relationship('ScanCategory')

    slices: List['Slice'] = relationship('Slice', back_populates='scan', order_by=lambda: Slice.location)
    labels: List['Label'] = relationship('Label', back_populates='scan')

    def __init__(self, category: ScanCategory) -> None:
        """Initialize Scan.

        :param category: Scan's category
        """
        self.id = ScanID(str(uuid.uuid4()))
        self.category = category

    def __repr__(self) -> str:
        """Return string representation for Scan."""
        return '<{}: {}: {}>'.format(self.__class__.__name__, self.id, self.category.key)

    def add_slice(self) -> 'Slice':
        """Add new slice into this Scan.

        :return: ID of a Slice
        """
        with db_session() as session:
            new_slice = Slice()
            new_slice.scan = self
            session.add(new_slice)
        return new_slice


class Slice(Base):
    """Definition of a Slice."""

    __tablename__ = 'Slices'
    id: SliceID = Column(String, primary_key=True)
    location: float = Column(Float, nullable=True)
    position_x: float = Column(Float, nullable=True)
    position_y: float = Column(Float, nullable=True)
    position_z: float = Column(Float, nullable=True)
    stored: bool = Column(Boolean, default=False)
    converted: bool = Column(Boolean, default=False)

    scan_id: ScanID = Column(String, ForeignKey('Scans.id'))
    scan: Scan = relationship('Scan', back_populates='slices')

    def __init__(self, location: SliceLocation = None, position: SlicePosition = None) -> None:
        """Initialize Slice.

        :param location: location of a Slice (useful for sorting)
        :param position: position of a Slice inside of a patient body
        """
        self.id = SliceID(str(uuid.uuid4()))
        if location:
            self.location = location
        if position:
            self.position_x = position.x
            self.position_y = position.y
            self.position_z = position.z

    def __repr__(self) -> str:
        """Return string representation for Slice."""
        return '<{}: {}: {}>'.format(self.__class__.__name__, self.id, self.location)

    def update_location(self, new_location: SliceLocation) -> 'Label':
        """Update location in the Slice."""
        self.location = new_location
        self.save()
        return self

    def update_position(self, new_position: SlicePosition) -> 'Label':
        """Update position in the Slice."""
        self.position_x = new_position.x
        self.position_y = new_position.y
        self.position_z = new_position.z
        self.save()
        return self

    def mark_as_stored(self) -> 'Label':
        """Mark Slice as stored in HBase."""
        self.stored = True
        self.save()
        return self

    def mark_as_converted(self) -> 'Label':
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
    status: LabelStatus = Column(Enum(LabelStatus), nullable=False, server_default=LabelStatus.NOT_VERIFIED.value)
    scan: Scan = relationship('Scan', back_populates='labels')
    selections: 'LabelSelection' = relationship('LabelSelection', back_populates='label')

    def __init__(self) -> None:
        """Initialize Label.

        By default all of the labels are not verified
        """
        self.id = LabelID(str(uuid.uuid4()))
        self.status = LabelStatus.NOT_VERIFIED

    def __repr__(self) -> str:
        """Return string representation for Label."""
        return '<{}: {}: {} {}>'.format(self.__class__.__name__, self.id, self.scan_id, self.status)

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

    label_id: LabelID = Column(String, ForeignKey('Labels.id'))
    label: Label = relationship('Label', back_populates='selections')

    def __init__(self, position: LabelPosition, shape: LabelShape) -> None:
        """Initialize Label Selection.

        :param position: position (x, y, slice_index) of the label
        :param shape: shape (width, height) of the label
        """
        self.id = LabelSelectionID(str(uuid.uuid4()))
        self.position_x = position.x
        self.position_y = position.y
        self.slice_index = position.slice_index
        self.shape_width = shape.width
        self.shape_height = shape.height

    def __repr__(self) -> str:
        """Return string representation for Label Selection."""
        return '<{}: {}>'.format(self.__class__.__name__, self.id)
