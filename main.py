import config as cfg
from sqlalchemy import create_engine, insert
from sqlalchemy import MetaData, Table, Column, ForeignKey
from sqlalchemy import Integer, String, DateTime, Numeric
from sqlalchemy.sql import func

engine = create_engine(
    f"postgresql://{cfg.db_user}:{cfg.db_password}@{cfg.db_host}:{cfg.db_port}/{cfg.database}",
    echo=True,
    future=True
)

md = MetaData()

vehicles = Table(
    "vehicles",
    md, 
    Column("vid", Integer, primary_key=True),
    Column("license_plate", String(6)),
    Column("owner_id", ForeignKey("users.uid"))
)
users = Table(
    "users",
    md,
    Column("uid", Integer, primary_key=True),
    Column("first_name", String(40)),
    Column("last_name", String(40))
)
transfers = Table(
    "transfers",
    md,
    Column("tid", Integer, primary_key=True),
    Column("time_of_transfer", DateTime, server_default=func.now()),
    Column("kwh_transferred", Numeric),
    Column("recipient_id", ForeignKey("vehicles.vid")),
    Column("donor_id", ForeignKey("vehicles.vid"))
)

def create_users():
    with engine.begin() as c:
        c.execute(
            insert(users),
            [
                {"first_name": "joe", "last_name": "bob"},
                {"first_name": "alison", "last_name": "nosila"},
            ]
        )
def create_vehicles():
    with engine.begin() as c:
        c.execute(
            insert(vehicles),
            [
                {"license_plate": "JOEBOB", "owner_id": 1},
                {"license_plate": "SONALI", "owner_id": 2}
            ]
        )


#md.create_all(engine)
#create_users();
#create_vehicles();

def record_transfer(did, rid, kwht):
    """records a transfer of energy in kwh from donor vehicle (did) to recipient vehicle (rid) at current time"""
    stmt = insert(transfers).values(donor_id=did, recipient_id=rid, kwh_transferred=kwht)
    print(stmt)
    with engine.begin() as c:
        c.execute(stmt)

record_transfer(1, 2, 134.12)

