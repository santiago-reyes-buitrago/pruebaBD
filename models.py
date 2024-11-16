from sqlalchemy import String,BIGINT,Column
from database import Bd

class usuarios(Bd):
    __tablename__ = "usuario"
    id = Column(BIGINT, primary_key=True,autoincrement=True)
    name = Column(String(50))

