"""Module responsible for defining all of the relational database models"""
import uuid
from typing import List

from dicom.dataset import FileDataset
from flask_user import UserMixin
from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship

from data_labeling.types import ScanID, SliceID, SliceLocation, SlicePosition
from data_labeling.database import Base, db_session
from data_labeling.clients.hbase_client import HBaseClient
from data_labeling.workers.storage import store_dicom
from data_labeling.workers.conversion import convert_dicom_to_png


class User(Base, UserMixin):
    """Defines model for the Users table entry"""
    __tablename__ = 'Users'
    id: int = Column(Integer, autoincrement=True, primary_key=True)
    username: str = Column(String(50), nullable=False, unique=True)
    password: str = Column(String(255), nullable=False, server_default='')

    def __init__(self, username: str, password_hash: str) -> None:
        """Initializer for a User

        :param username: user's name
        :param password_hash: user's password (already hashed)
        """
        self.username = username
        self.password = password_hash

    def __repr__(self) -> str:
        """String representation for User"""
        return '<{}: {}: {}>'.format(self.__class__.__name__, self.id, self.username)


class Scan(Base):  # pylint: disable=too-few-public-methods
    """Definition of a Scan"""
    __tablename__ = 'Scans'
    id: ScanID = Column(String, primary_key=True)

    slices: List['Slice'] = relationship('Slice', back_populates='scan', order_by=lambda: Slice.location)

    def __init__(self) -> None:
        """Initializer for Scan"""
        self.id = ScanID(str(uuid.uuid4()))

    def __repr__(self) -> str:
        """String representation for Scan"""
        return '<{}: {}>'.format(self.__class__.__name__, self.id)

    def add_slice(self, dicom_image: FileDataset) -> None:
        """Add new slice into this Scan

        It will also trigger Celery workers responsible for storage and conversion of a Dicom image.

        :param dicom_image: Dicom image that should be stored for this Scan
        """
        location = SliceLocation(dicom_image.SliceLocation)
        position = SlicePosition(dicom_image.ImagePositionPatient[0],
                                 dicom_image.ImagePositionPatient[1],
                                 dicom_image.ImagePositionPatient[2])

        with db_session() as session:
            new_slice = Slice(location, position)
            new_slice.scan = self
            session.add(new_slice)

        store_dicom.delay(new_slice.id, dicom_image)
        convert_dicom_to_png.delay(new_slice.id, dicom_image)


class Slice(Base):
    """Definition of a Slice"""
    __tablename__ = 'Slices'
    id: SliceID = Column(String, primary_key=True)
    location: float = Column(Float, nullable=False)
    position_x: float = Column(Float, nullable=False)
    position_y: float = Column(Float, nullable=False)
    position_z: float = Column(Float, nullable=False)

    scan_id: ScanID = Column(String, ForeignKey('Scans.id'))
    scan: Scan = relationship('Scan', back_populates='slices')

    def __init__(self, location: SliceLocation, position: SlicePosition) -> None:
        """Initializer for Slice

        :param location: location of a Slice (useful for sorting)
        :param position: position of a Slice inside of a patient body
        """
        self.id = SliceID(str(uuid.uuid4()))
        self.location = location
        self.position_x = position.x
        self.position_y = position.y
        self.position_z = position.z

        self.hbase_client = HBaseClient()

    def __repr__(self) -> str:
        """String representation for Slice"""
        return '<{}: {}: {}>'.format(self.__class__.__name__, self.id, self.location)

    @property
    def original_image(self) -> bytes:
        """Return original Dicom image as bytes"""
        if not hasattr(self, 'hbase_client'):
            self.hbase_client = HBaseClient()
        data = self.hbase_client.get(HBaseClient.ORIGINAL_SLICES_TABLE, self.id, columns=['image'])
        return data[b'image:value']

    @property
    def converted_image(self) -> bytes:
        """Return converted image as bytes"""
        if not hasattr(self, 'hbase_client'):
            self.hbase_client = HBaseClient()
        data = self.hbase_client.get(HBaseClient.CONVERTED_SLICES_TABLE, self.id, columns=['image'])
        return data[b'image:value']
