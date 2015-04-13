from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import mapper, relation

engine = create_engine("postgresql+psycopg2://localhost:5432/textura", echo=False)

metadata = MetaData()
metadata.reflect(bind=engine)
