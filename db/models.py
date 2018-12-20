from sqlalchemy import create_engine, Column, Integer, String, UniqueConstraint
from sqlalchemy import NUMERIC, ForeignKey, DateTime, Float
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from datetime import datetime

from settings import DATABASES

ENGEINE = create_engine(URL(**DATABASES['POSTGRES']))
SESSION = sessionmaker(bind=ENGEINE)
Base = declarative_base()

class FirmInfo(Base):
    __tablename__ = 'firm_info'
    id = Column(Integer, primary_key=True)
    juristic_name = Column(String(30), nullable=False)
    inn = Column(NUMERIC, nullable=False)
    kpp = Column(NUMERIC, nullable=False)
    UniqueConstraint(juristic_name)
    UniqueConstraint(inn, kpp)

    def __repr__(self):
        return "<Firm(id='%s', jujistic='%s')>" % (self.id, self.juristic_name)


class UserInfo(Base):
    __tablename__ = 'user_info'
    id = Column(Integer, primary_key=True)
    firm_id = Column(Integer, ForeignKey('firm_info.id'), nullable=True)
    telegram_id = Column(Integer, nullable=False)
    name = Column(String(25), nullable=False)
    nickname = Column(String(15), nullable=False)
    email = Column(String(20), nullable=False)
    permission = Column(Integer, default=0, nullable=False)
    last_query_time = Column(DateTime, nullable=True)
    UniqueConstraint(nickname)
    ACCESS = 10
    NOT_REGISTRED = 0
    BAN = -5
    WAITING = 5
    def __repr__(self):
        return "<User(id='%s', name='%s')>" % (self.id, self.name)


class Container(Base):
    __tablename__ = 'container'
    id = Column(String(11), nullable=False, primary_key=True)
    comment = Column(String)
    gps_last_time = Column(DateTime, default=datetime.now())
    customs_last_time = Column(DateTime, default=datetime.now())

    def __repr__(self):
        return "<Container(id='%s')>" % self.id


class UserContainer(Base):
    __tablename__ = 'user_container'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_info.id'), nullable=False)
    cont_id = Column(String(11), ForeignKey('container.id'), nullable=False)
    chat_id = Column(Integer, nullable=False)
    last_customs_state = Column(String)
    UniqueConstraint(user_id, cont_id)

    def __repr__(self):
        return "<User_Container(user='%s', cont='%s')>" % (
            self.user_id,
            self.cont_id
        )


class TelemetryState(Base):
    __tablename__ = 'telemetry_state'
    id = Column(Integer, primary_key=True)
    cont_id = Column(String(11), ForeignKey('container.id'), nullable=False)
    received_time = Column(DateTime, default=datetime.now())
    modem_signal = Column(Integer, nullable=False)
    temperature = Column(Float, nullable=False)
    location_age = Column(Integer, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    date_raw = Column(Integer, nullable=False)
    time_raw = Column(Integer, nullable=False)
    speed = Column(Float, nullable=False)

    def __repr__(self):
        return "<Telemetry(id='%s', cont_id='%s')>" % (self.id, self.cont_id)


# class CustomsState(Base):
#     __tablename__ = 'customs_state'
#     id = Column(Integer, primary_key=True)
#     cont_id = Column(String(11), ForeignKey('container.id'), nullable=False)
#     received_time = Column(DateTime, default=datetime.now())
#     status = Column(String, nullable=False)
#
#     def __repr__(self):
#         return "<Customs(id='%s', cont_id='%s')>" % (self.id, self.cont_id)
#Base.metadata.create_all(ENGEINE)