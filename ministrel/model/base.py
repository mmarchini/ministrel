from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

dburi = "postgresql+psycopg2://matheus:minstrel@localhost:5432/minstrel"
engine = create_engine(dburi, echo=True)
Session = sessionmaker(bind=engine, autocommit=True)

Base = declarative_base()

session = Session()
