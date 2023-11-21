#IN THIS FILE WE HAVE CONNECTED THE SQLITE DATABASE TO THE PROJECT :
#FOR THIS WE HAVE DOWNLOADED  'sqlachemy' IN OUR MAIN FOLDER
#COMMAND { python install sqlalchemy }. This file is stored in fastapienv inside the libs

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:somya@localhost/TodoApplicationDatabase" #stores the database

engine = create_engine(
SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False ,autoflush=False ,bind=engine)

Base =declarative_base()
