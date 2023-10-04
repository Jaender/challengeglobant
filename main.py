# Importar librerias de FastAPI
from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.security import HTTPBearer
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder

# Importar librerias para los mdoelos de datos y la validacíon
from pydantic import BaseModel, Field
from typing import Optional,List
from config.base_de_datos import sesion, motor, base

# Importar libreria para la autenticación
from jwt_config import dame_token,valida_token

# Importar modelo de datos de prueba
from modelos.ventas import Ventas as VentasModelo

# Importar modelos de datos ejercicio
from modelos.ventas import Jobs as JobsModelo
from modelos.ventas import Hired as HiredModelo
from modelos.dep import Depart as DepModelo

#Importar pandas para manipulación de datos
import pandas as pd

# crea instancia de fastapi y datos de documentación
app = FastAPI()
app.title = 'Aplicacion de ventas'
app.version = '1.0.1'
base.metadata.create_all(bind=motor)

# Creo array de prueba 
ventas = [
    {
        "id": 1,
        "fecha": "01/01/23",
        "tienda": "Tienda01",
        "importe": 2500
    },
    {
        "id": 2,
        "fecha": "22/01/23",
        "tienda": "Tienda02",
        "importe": 4500
    }
]
# Creo array modelo para ingreso de datos uno a uno 
Job = [
    {
        "id": 1,
        "job": "Marketing Assistant"
    }
]
Depart = [
    {
        "id": 1,
        "department": "Product Management"
    }
]
Hired = [
    {
        "id": 1,
        "name": "Harold Vogt",
        "datetime": "2021-11-07T02:48:42Z",
        "department_id": 2,
        "job_id": 96        
    }
]

# Creo los modelos de BD
class Job(BaseModel):
    id:int = Field(ge=0, le=200)
    job:str = Field(min_length=4, max_length=100)
class Depart(BaseModel):
    id:int = Field(ge=0, le=200)
    department:str = Field(min_length=4, max_length=200)
class Hired(BaseModel):
    id:int = Field(ge=0, le=200)
    name:str = Field(min_length=4, max_length=300)
    datetime:str = Field(min_length=4, max_length=300)
    department_id:int = Field(ge=0, le=200)
    job_id:int = Field(ge=0, le=200)
class Usuario(BaseModel):
    email:str
    clave:str
class Ventas(BaseModel):
    #id: int = Field(ge=0, le=20)
    id: Optional[int]=None
    fecha: str
    #tienda: str = Field(default="Tienda01",min_length=4, max_length=10)
    tienda: str = Field(min_length=4, max_length=10)
    #tienda:str
    importe:float
    class Config:
        schema_extra = {
            "example":{
                "id":1,
                "fecha":"01/02/23",
                "tienda":"Tienda09",
                "importe":131
            }
        }
        
# Portador token
class Portador(HTTPBearer):
    async def __call__(self, request:Request):
        autorizacion = await super().__call__(request)
        dato = valida_token(autorizacion.credentials)
        if dato['email'] != 'ja@gmail.com':
            raise HTTPException(status_code=403, detail='No autorizado')

# crear punto de entrada o endpoint


#@app.get('/', tags=['Inicio'])  # cambio de etiqueta en documentacion
#def mensaje():
#    return HTMLResponse('<h2>Titulo html desde FastAPI</h2>')


#@app.get('/ventas', tags=['Ventas'], response_model=List[Ventas], status_code=200, dependencies=[Depends(Portador())])
#def dame_ventas() -> List[Ventas]:
#    db = sesion()
#    resultado = db.query(VentasModelo).all()
#    return JSONResponse(status_code=200,content=jsonable_encoder(resultado))


#@app.get('/ventas/{id}', tags=['Ventas'], response_model = Ventas, status_code = 200)
#def dame_ventas(id: int = Path(ge=1,le=1000)) -> Ventas:
#    db = sesion()
#    resultado = db.query(VentasModelo).filter(VentasModelo.id == id).first()
#    if not resultado:
#        return JSONResponse(status_code=404, content={'mensaje':'No se encontro ese identificador'})
    
#    return JSONResponse(status_code=200, content=jsonable_encoder(resultado)) 

#@app.get('/ventas/', tags=['Ventas'], response_model=List[Ventas], status_code=200)
# para mas parametros ,id:int
#def dame_ventas_por_tienda(tienda: str = Query(min_length=4, max_length=20)) -> List[Ventas]:
    # return tienda0l
    
#    db = sesion()
#    resultado = db.query(VentasModelo).filter(VentasModelo.tienda == tienda).all()
#    if not resultado:
#        return JSONResponse(status_code=404, content={'mensaje': 'No se encontro esa tienda'})
#    return JSONResponse(content = jsonable_encoder(resultado))

#@app.post('/ventas', tags=['Ventas'], response_model=dict, status_code=201)
#def crea_venta(venta:Ventas) -> dict:
#    db = sesion()
    # extraemos atributos para paso como parametros
#    nueva_venta = VentasModelo(**venta.dict())
    # añadir a bd y hacemos commit para actualizar datos
#    db.add(nueva_venta)
#    db.commit()
#    return JSONResponse(content={'mensaje': 'Venta registrada'}, status_code=200)

#@app.put('/ventas/{id}', tags=['Ventas'], response_model=dict, status_code=201)
#def actualiza_ventas(id: int, venta: Ventas) -> dict:
    # recorrer los elementos de la lista
    
#    for elem in ventas:        
#        if elem['id'] == id:
#           elem['fecha'] = venta.fecha
#           elem['tienda'] = venta.tienda
#           elem['importe'] = venta.importe
#    return JSONResponse(content={'mensaje': 'Venta actualizada'}, status_code=201)


#@app.delete('/ventas/{id}', tags=['Ventas'], response_model=dict, status_code=200)
#def borra_venta(id: int) -> dict:
    # recorremos elementos de la lista
#    for elem in ventas:
#        if elem['id'] == id:
#            ventas.remove(elem)
#    return JSONResponse(content={'mensaje':'Venta borrada'}, status_code=200)

#Creamos ruta para login
@app.post('/login',tags=['autenticacion'])
def login(usuario:Usuario):
    if usuario.email == 'ja@gmail.com' and usuario.clave == '12345':
        # obtenemos el token con la funcion pasandole el diccionario de usuario
        token:str=dame_token(usuario.dict())
        return JSONResponse(status_code=200,content=token) #Codigo de respuesta exitoso
    else:
        return JSONResponse(content={'mensaje':'Acceso denegado'}, status_code=404) #Código de respuesta no exitoso

# Métodos para Hired

@app.get('/hired', tags=['Hired'], response_model=List[Hired], status_code=200, dependencies=[Depends(Portador())])
def get_hired() -> dict: 
    db = sesion()
    hired_result = db.query(HiredModelo).all()
    return JSONResponse(status_code=200,content=jsonable_encoder(hired_result)) 

@app.post('/hired', tags=['Hired'], response_model=dict, status_code=201)
def new_hired(hired:Hired) -> dict:
    db = sesion()
    # extraemos atributos para paso como parametros
    new_hired = HiredModelo(**hired.dict())
    # añadir a bd y hacemos commit para actualizar datos
    db.add(new_hired)
    db.commit()
    return JSONResponse(content={'mensaje': 'Hired recorded'}, status_code=200)


# Métodos de Departamentos

@app.post('/departments', tags=['Departments'], response_model=dict, status_code=201)
def new_department(department:Depart) -> dict:
    db = sesion()
    # extraemos atributos para paso como parametros
    new_department = DepModelo(**department.dict())
    # añadir a bd y hacemos commit para actualizar datos
    #depa = pd.DataFrame(new_department)
    #print(depa)
    db.add(new_department)
    return JSONResponse(content={'mensaje': 'Department recorded'}, status_code=200)

#, dependencies=[Depends(Portador()) ]  
@app.get('/departments', tags=['Departments'], response_model=List[Depart], status_code=200)
def get_department() -> dict: 
    db = sesion()
    new_var = DepModelo
    department_result = db.query(new_var).all()
    return JSONResponse(status_code=200,content=jsonable_encoder(department_result)) 


# Métodos de Jobs

@app.get('/jobs', tags=['Jobs'], response_model=List[Job], status_code=200, dependencies=[Depends(Portador())]) #, dependencies=[Depends(Portador())]
def get_job() -> dict: 
    db = sesion()
    job_result = db.query(JobsModelo).all()
    return JSONResponse(status_code=200,content=jsonable_encoder(job_result))   
   
@app.post('/jobs', tags=['Jobs'], response_model=dict, status_code=201)
def new_job(job:Job) -> dict:
    db = sesion()
    # extraemos atributos para paso como parametros
    new_job = JobsModelo(**job.dict())
    # añadir a bd y hacemos commit para actualizar datos
    db.add(new_job)
    db.commit()
    return JSONResponse(content={'mensaje': 'Job recorded'}, status_code=200)

@app.post('/jobs/file', tags=['Jobs'], response_model=dict, status_code=201)
def new_job(job:Job) -> dict:
    db = sesion()
    # extraemos atributos para paso como parametros
    df = pd.read_csv('Jobs.csv', header=None, names=['id', 'job'])
    new_job = JobsModelo(**job.dict())
    
    for elem in df.index:
        #print(elem)
        serie = df.loc[df['id'] == elem]
        print(df.index[elem])
        new_job.id = df.index[elem]
        print(serie.job.values)
        new_job.job = serie.job.values
        db.add(new_job)
        db.commit()
    
 

    return JSONResponse(content={'mensaje': 'Jobs recorded'}, status_code=200)