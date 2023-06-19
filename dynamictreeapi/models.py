from .database import Base 
from sqlalchemy import Column, ForeignKey, Integer,String
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Dataset(Base):
    __tablename__ = "datasets"

    id =  Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    data = Column(String, nullable=False)
    url = Column(String, nullable=True)
    type = Column(String, server_default='raw',nullable=False)
    created_date = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("Users")

class Users(Base):
    __tablename__ = "users"

    id =  Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_date = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))


class Permissions(Base):
    __tablename__ = "users_datasets_permissions"

    user_id =  Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    dataset_id =  Column(Integer, ForeignKey("datasets.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    type = Column(String, nullable=False) 