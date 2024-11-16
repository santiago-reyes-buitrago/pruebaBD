from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from decouple import config

URL_DATABASE = f"mysql+pymysql://{config('MYSQL_USER')}:{config('MYSQL_PASSWORD')}@{config('MYSQL_HOST')}:{config('MYSQL_PORT')}/{config('MYSQL_BD')}"
print(URL_DATABASE)
engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Bd = declarative_base()
