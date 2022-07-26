import config as cfg
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, relationship, Session 
from sqlalchemy import and_, or_, select, inspect
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

    def __repr__(self):
        return f'vid: {self.vid}, license: {self.license_plate}, owner: {self.uid}'

class User(Base):
    __tablename__ = "users"
    uid = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    vehicles = relationship("Vehicle", back_populates="users")

    def __repr__(self):
        return f'{self.first_name} {self.last_name}, uid: {self.uid}'

    @classmethod
    def getVehicles(cls, uid):
        # returns a list of the user's vehicle objects 
        with Session(engine) as s:
            user = s.get(cls, uid)
            if user is None:
                raise ValueError(f'There is no user with id {uid}')
            return list(user.vehicles) # after returning i believe the vehicle objects are "detached" and lose their connection with the corresponding row?? 
    @classmethod
    def getTxs(cls, uid):
        # returns a list of the user's Tx objects (both receiving and donating)
        with Session(engine) as s:
            user = s.get(cls, uid)
            if user is None:
                raise ValueError(f'There is no user with id {uid}')
            stmt = select(Tx).where(or_(Tx.recipient_id == uid, Tx.donor_id == uid))
            txs = s.scalars(stmt)
            return list(txs)

class Tx(Base):
    __tablename__ = "transactions"
    tid = Column(Integer, primary_key=True)

    start_time = Column(DateTime)
    stop_time = Column(DateTime, server_default=func.now())
    recipient_id = Column(ForeignKey("vehicles.vid"))
    donor_id = Column(ForeignKey("vehicles.vid"))
    kwh_transferred = Column(Numeric)

    def __repr__(self):
        return f'{self.kwh_transferred} from vehicle {self.recipient_id} to vehicle {self.donor_id}; started at {self.start_time} and ended at {self.stop_time}'

class TxIP(Base): # transactions in progress
    __tablename__ = "tx_in_progress"
    txip_id = Column(Integer, primary_key=True)
    time = Column(DateTime, server_default=func.now())
    recipient_id = Column(ForeignKey("vehicles.vid"))
    donor_id = Column(ForeignKey("vehicles.vid"))

    
    @classmethod
    def start(cls, rid, did):
        # returns the id of the txip created; this is used to stop the txip later
        with Session(engine) as s: 
            # test if there is already a TxIP from donor to recipient
            stmt = select(1).where(and_(TxIP.recipient_id == rid, TxIP.donor_id == did))
            if s.execute(stmt).first() is not None:
                raise ValueError(f'There is already a Tx in progress from vehicle {did} to vehicle {rid}')
            
            newTxIP = cls(recipient_id=rid, donor_id=did)
            s.add(newTxIP)
            s.commit()
            return newTxIP.txip_id
    @classmethod
    def stop(cls, id):
        with Session(engine) as s:
            txip = s.get(cls, id)
            if txip is None:
                raise ValueError(f'There is no Tx currently in progress with id {id}')
            
            # can't use python's datetime.now(), i realized that datetime.now() is out of sync with yugabyte's now() [yugabyte is ahead by 4 hours]
            newTx = Tx(start_time=txip.time, recipient_id=txip.recipient_id, donor_id=txip.donor_id)
            s.add(newTx)
            s.flush() # we need to flush so that newTx gets it's stop_time before we computer kwh_transferred
            # right now the kwh_transferred is just the number of seconds that have passed; this should be replaced in the future
            newTx.kwh_transferred = (newTx.stop_time - txip.time).total_seconds() 
            
            s.delete(txip)
            s.commit()

# Base.metadata.create_all(engine)

def createTestObjects():
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





