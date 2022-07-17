import config as cfg
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table, Column
from sqlalchemy import Integer

engine = create_engine(
    f"postgresql://{cfg.db_user}:{cfg.db_password}@{cfg.db_host}:{cfg.db_port}/{cfg.database}",
    echo=True,
    future=True
)

md = MetaData()
test = Table(
    "test",
    md, 
    Column("x", Integer, primary_key=True),
    Column("y", Integer)
)

# md.create_all(engine)

