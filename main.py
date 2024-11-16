from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import SessionLocal
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


class IngresoBase(BaseModel):
    name: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

# Configuración de CORS
origins = [
    "*"
    # Agrega otros orígenes si es necesario
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def index():
    return {"message": "Hello World"}


@app.get("/prestamo", status_code=status.HTTP_200_OK)
async def getPrestamos(db: db_dependency):
    registros = db.query(models.usuarios).all()
    return registros


@app.get("/prestamo/{id}", status_code=status.HTTP_200_OK)
async def getPrestamo(id: int, db: db_dependency):
    registro = db.query(models.usuarios).filter(models.usuarios.id == id).first()
    if registro is None:
        return HTTPException(status_code=404, detail="Registro no encontrado")
    return registro


@app.post("/prestamo", status_code=status.HTTP_201_CREATED)
async def postPrestamo(registro: IngresoBase, db: db_dependency):
    db_registro = models.usuarios(**registro.model_dump())
    db.add(db_registro)
    db.commit()
    return "Se creo exitosamente un prestamo"


@app.put("/prestamo/{id}")
async def putPrestamo(registro: IngresoBase, id: int, db: db_dependency):
    registroActualizado = db.query(models.usuarios).filter(models.usuarios.id == id).first()
    if registroActualizado is None:
        return HTTPException(status_code=404, detail="No se encuentra el registro")
    registroActualizado.name = registro.name
    db.commit()
    return "Registro actualizado exitosamente"


@app.delete("/prestamo/{id}", status_code=status.HTTP_200_OK)
async def deletePrestamo(id: int, db: db_dependency):
    registro = db.query(models.usuarios).filter(models.usuarios.id == id).first()
    if registro is None:
        return HTTPException(status_code=404, detail="No se puede borar el registro")
    db.delete(registro)
    db.commit()
    return 'El registro se elimino exitosamente'
