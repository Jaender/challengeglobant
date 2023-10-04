from config.base_de_datos import base
from sqlalchemy import Column, Integer, String, Float

class Depart(base):
    # nombre de la tabla
    __tablename__ = "depart"
    id = Column(Integer, primary_key= True)
    department = Column(String)