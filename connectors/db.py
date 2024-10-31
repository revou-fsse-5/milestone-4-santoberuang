from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
print('connecting to database...')

engine = create_engine(f'mysql+pymsql://milestone4santo_togetheras:aea57cc0af2e83cd579446184cd7bc1d82c3aa21@cpu2s.h.filess.io:3307/milestone4santo_togetheras')

connection = engine.connect()
print('connected to database')

Session = sessionmaker(connection)