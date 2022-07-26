import config as cfg
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, relationship, Session 
from sqlalchemy import and_, select
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, DateTime, Numeric
from sqlalchemy.sql import func

engine = create_engine(
    f"postgresql://{cfg.db_user}:{cfg.db_password}@{cfg.db_host}:{cfg.db_port}/{cfg.database}",
    echo=True,
    future=True
)

Base = declarative_base();
class Vehicle(Base):
    __tablename__ = "vehicles"
    vid = Column(Integer, primary_key=True)
    license_plate = Column(String(6))
    uid = Column(Integer, ForeignKey("users.uid"))

    users = relationship("User", back_populates="vehicles")

class User(Base):
    __tablename__ = "users"
    uid = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    vehicles = relationship("Vehicle", back_populates="users")

class Tx(Base):
    __tablename__ = "transactions"
    tid = Column(Integer, primary_key=True)

    start_time = Column(DateTime)
    stop_time = Column(DateTime)
    recipient_id = Column(ForeignKey("vehicles.vid"))
    donor_id = Column(ForeignKey("vehicles.vid"))
    kwh_transferred = Column(Numeric)

class TxIP(Base): # transactions in progress
    __tablename__ = "tx_in_progress"
    txip_id = Column(Integer, primary_key=True)
    time = Column(DateTime, server_default=func.now())
    recipient_id = Column(ForeignKey("vehicles.vid"))
    donor_id = Column(ForeignKey("vehicles.vid"))

    
    @classmethod
    def startTxIP(cls, recipient_id, donor_id):
        with Session(engine) as s: # test if there is already a TxIP from donor to recipient
            stmt = select(1).where(and_(TxIP.recipient_id == recipient_id, TxIP.donor_id == donor_id))
            if s.execute(stmt).first() is not None:
                raise ValueError(f'There is already a Tx in progress from vehicle {donor_id} to vehicle {recipient_id}')
    @classmethod
    def stopTxIP(cls):
        with Session(engine) as s:
            

# Base.metadata.create_all(engine)

TxIP.startTxIP(101, 102)


"""
with Session(engine) as s:
    u1 = User(first_name="Joe", last_name="Bob")
    u2 = User(first_name="Alice", last_name="Allie")

    v1 = Vehicle(license_plate="JJJBBB")
    v2 = Vehicle(license_plate="BBBJJJ")
    v3 = Vehicle(license_plate="AAAAAA")

    u1.vehicles.append(v1)
    u1.vehicles.append(v2)
    u2.vehicles.append(v3)

    s.add(u1)
    s.add(u2)
    s.commit()
"""



