from fastapi import FastAPI, Request, Form, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from datetime import datetime
from app.routers import users
from app.models.user import UserCreate, UserUpdate

app = FastAPI(
    title="Mi Primera API",
    description="API de ejemplo para aprender FastAPI",
    version="1.0.0"
)

# Configurar archivos estáticos y templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Incluir routers de la API
app.include_router(users.router, prefix="/api/v1", tags=["usuarios"])

# Importar la base de datos desde users para accederla
from app.routers.users import fake_users_db, next_id

# RUTAS PARA LA INTERFAZ WEB
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    total_users = len(fake_users_db)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "total_users": total_users
    })

@app.get("/users", response_class=HTMLResponse)
async def users_page(request: Request):
    return templates.TemplateResponse("users_list.html", {
        "request": request,
        "users": fake_users_db
    })

@app.get("/users/create", response_class=HTMLResponse)
async def create_user_page(request: Request):
    return templates.TemplateResponse("create_user.html", {
        "request": request
    })

@app.post("/users/create")
async def create_user_form(
    request: Request,
    nombre: str = Form(...),
    email: str = Form(...),
    edad: int = Form(...),
    cedula: str = Form(...),
    password: str = Form(...)
):
    try:
        # Verificar si el email ya existe
        for existing_user in fake_users_db:
            if existing_user["email"] == email:
                return templates.TemplateResponse("create_user.html", {
                    "request": request,
                    "messages": [{"type": "danger", "content": "El email ya está registrado"}]
                })
        
        # Crear usuario usando la misma lógica que la API
        user_data = UserCreate(nombre=nombre, email=email, edad=edad, cedula=cedula, password=password)
        
        global next_id
        new_user = {
            "id": next_id,
            "nombre": user_data.nombre,
            "email": user_data.email,
            "edad": user_data.edad,
            "cedula": user_data.cedula,
            "fecha_creacion": datetime.now(),
            "activo": True
        }
        
        fake_users_db.append(new_user)
        next_id += 1
        
        return RedirectResponse(url="/users", status_code=status.HTTP_302_FOUND)
        
    except Exception as e:
        return templates.TemplateResponse("create_user.html", {
            "request": request,
            "messages": [{"type": "danger", "content": f"Error: {str(e)}"}]
        })

@app.get("/users/{user_id}/edit", response_class=HTMLResponse)
async def edit_user_page(request: Request, user_id: int):
    user = None
    for u in fake_users_db:
        if u["id"] == user_id:
            user = u
            break
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    return templates.TemplateResponse("edit_user.html", {
        "request": request,
        "user": user
    })

@app.post("/users/{user_id}/edit")
async def edit_user_form(
    request: Request,
    user_id: int,
    nombre: str = Form(None),
    email: str = Form(None),
    edad: int = Form(None),
    cedula: str = Form(None),
    activo: str = Form(None)
):
    try:
        # Encontrar usuario
        user_index = None
        for i, user in enumerate(fake_users_db):
            if user["id"] == user_id:
                user_index = i
                break
        
        if user_index is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Actualizar campos
        if nombre:
            fake_users_db[user_index]["nombre"] = nombre
        if email:
            fake_users_db[user_index]["email"] = email
        if edad:
            fake_users_db[user_index]["edad"] = int(edad)
        if cedula:
            fake_users_db[user_index]["cedula"] = cedula
        
        fake_users_db[user_index]["activo"] = activo == "on"
        
        return RedirectResponse(url="/users", status_code=status.HTTP_302_FOUND)
        
    except Exception as e:
        user = fake_users_db[user_index] if user_index is not None else {}
        return templates.TemplateResponse("edit_user.html", {
            "request": request,
            "user": user,
            "messages": [{"type": "danger", "content": f"Error: {str(e)}"}]
        })

# Ruta de la API original (solo para JSON)
@app.get("/api")
async def api_root():
    return {"mensaje": "¡Bienvenida a tu primera API, Camila!"}

@app.get("/health")
async def health_check():
    return {"estado": "activo", "version": "1.0.0"}