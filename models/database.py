from sqlalchemy import Column, Integer, Enum, Unicode, UnicodeText, String, ForeignKey, PickleType
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class FellowDb(Base):
    __tablename__ = 'fellows'

    id = Column(Integer, primary_key=True)
    person_name = Column(String(50))
    person_id = Column(Integer)

    def __init__(self, person_name, person_id):
        self.person_name = person_name
        self.person_id = person_id



class StaffDb(Base):

    __tablename__ = 'staff'

    person_name = Column(String)
    person_id = Column(Integer, primary_key=True)

    def __init__(self, person_name, person_id):
        self.person_name = person_name
        self.person_id = person_id


class OfficeblockDb(Base):

    __tablename__ = 'officeblock'
    room_name = Column(String, primary_key=True)
    room_occupants = Column(String)

    def __init__(self, room_name, room_occupants):
        self.room_name = room_name
        self.room_occupants = room_occupants


class LivingspaceDb(Base):

    __tablename__ = 'livingspace'
    room_name = Column(String, primary_key=True)
    room_occupants = Column(String)

    def __init__(self, room_name, room_occupants):
        self.room_name = room_name
        self.room_occupants = room_occupants


class UnallocatedDb(Base):
    __tablename__ = 'unallocated'
    person_name = Column(String)
    person_id = Column(Integer, primary_key=True)
    person_type = Column(String)

    def __init__(self, person_name, person_id, person_type):
        self.person_name = person_name
        self.person_id = person_id
        self.person_type = person_type


class PersonelIdsDb(Base):
    __tablename__ = 'personelid'

    current_id = Column(Integer, primary_key=True)

    def __init__(self, current_id):
        self.current_id = current_id
