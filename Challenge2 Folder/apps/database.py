from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///mofa.db")

class Ingredient(Base):
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    quantity = Column(Float)

class Recipe(Base):
    __tablename__= 'recipes'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    ingredients = Column(String)
    taste = Column(String)
    cuisine_type = Column(String)
    preparation_time = Column(Integer)
    instructions = Column(String)

Base.metadata.create_all(engine)