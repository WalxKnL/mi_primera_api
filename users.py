from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.user import UserCreate, UserResponse, UserUpdate
from datetime import datetime

router = APIRouter()

# Base de datos simulada en memoria
fake_users_db = []
next_id = 1

@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def crear_usuario(user: UserCreate):
    global next_id
    
    # Verificar si el email ya existe
    for existing_user in fake_users_db:
        if existing_user["email"] == user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
    
    # Verificar si la cédula ya existe
    for existing_user in fake_users_db:
        if existing_user["cedula"] == user.cedula:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La cédula ya está registrada"
            )
    
    # Crear nuevo usuario
    new_user = {
        "id": next_id,
        "nombre": user.nombre,
        "email": user.email,
        "edad": user.edad,
        "cedula": user.cedula,
        "fecha_creacion": datetime.now(),
        "activo": True
    }
    
    fake_users_db.append(new_user)
    next_id += 1
    
    return new_user

@router.get("/users", response_model=List[UserResponse])
async def obtener_usuarios():
    return fake_users_db

@router.get("/users/{user_id}", response_model=UserResponse)
async def obtener_usuario(user_id: int):
    for user in fake_users_db:
        if user["id"] == user_id:
            return user
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )

@router.put("/users/{user_id}", response_model=UserResponse)
async def actualizar_usuario(user_id: int, user_update: UserUpdate):
    for i, user in enumerate(fake_users_db):
        if user["id"] == user_id:
            # Actualizar solo los campos proporcionados
            if user_update.nombre is not None:
                fake_users_db[i]["nombre"] = user_update.nombre
            if user_update.email is not None:
                fake_users_db[i]["email"] = user_update.email
            if user_update.edad is not None:
                fake_users_db[i]["edad"] = user_update.edad
            if user_update.cedula is not None:
                fake_users_db[i]["cedula"] = user_update.cedula
            if user_update.activo is not None:
                fake_users_db[i]["activo"] = user_update.activo
            
            return fake_users_db[i]
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_usuario(user_id: int):
    for i, user in enumerate(fake_users_db):
        if user["id"] == user_id:
            del fake_users_db[i]
            return
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )