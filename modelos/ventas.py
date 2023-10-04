# Importar librerias para crear las tablas de base de datos
from config.base_de_datos import base
from sqlalchemy import Column, Integer, String, Float

class Ventas(base):
    # nombre de la tabla
    __tablename__ = "ventas"
    id = Column(Integer, primary_key= True)
    fecha = Column(String)
    tienda = Column(String)
    importe = Column(Float)
    
class Jobs(base):
    # nombre de la tabla
    __tablename__ = "jobs"
    id = Column(Integer, primary_key= True)
    job = Column(String)
    
class Hired(base):
    # nombre de la tabla
    __tablename__ = "hired"
    id = Column(Integer, primary_key= True)
    name = Column(String)
    datetime = Column(String)
    department_id = Column(Integer)
    job_id = Column(Integer)