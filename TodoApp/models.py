#IN THIS FILE WE HAVE CREATED AN SCHEMA FOR THE DATABASE EGICH INCLUDES THE FOLLOWING DETAILS:
# 1) ID
# 2) TITLE OF THE WORK THAT WE HAVE TO COMPLETE
# 3) DESCRIPTION OF THE WORK
# 4) PRIORITY OF THE TASK
# 5) CURRENT STATUS OF THE TASK (COMPLETED OR NOT)

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base #described in database file

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String , unique=True , index=True)
    username = Column(String , unique=True , index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean ,default=True) #it will tterminate the session if the use is not active

    TODOS = relationship("Todos" ,back_populates="owner")

class Todos(Base):
    __tablename__  ="TODOS"

    id = Column(Integer,primary_key=True , index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    status = Column(Boolean ,default=True)

    owner_id = Column( Integer , ForeignKey("users.id"))

    owner = relationship("User" , back_populates="TODOS")