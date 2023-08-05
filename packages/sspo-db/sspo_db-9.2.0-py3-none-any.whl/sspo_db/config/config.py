from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from pprint import pprint
import sys

try:
    SQLALCHEMY_DATABASE_URI = f"postgres://{sys.argv[1]}:{sys.argv[2]}@{sys.argv[3]}/{sys.argv[4]}"
    # SQLALCHEMY_DATABASE_URI = "postgres://postgres:1234@localhost/sro_ontology"
except Exception as e:
    pprint("ERROR: 4 parameters are needed: <User> <Password> <Host> <Database>")
    exit(1)

engine = create_engine(SQLALCHEMY_DATABASE_URI)
session = sessionmaker(bind=engine)
session = session()
Base = declarative_base()

class Config():

    def create_database(self):
        Base.metadata.create_all(engine)

