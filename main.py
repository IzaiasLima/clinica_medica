from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse

import db

app = FastAPI()
app.mount("/app", StaticFiles(directory="static", html="True"), name="static")


@app.get("/", response_class=RedirectResponse)
async def root():
    return "/app/login.html"


@app.get("/api", response_class=RedirectResponse)
async def root():
    return "/app/login.html"


@app.get("/api/pacientes", response_class=JSONResponse)
async def pacientes():
    dados = db.get_pacientes()
    return dados


@app.get("/api/medicos")
async def medicos():
    dados = db.get_medicos()
    return dados


@app.delete("/api/medicos/{id}", response_class=HTMLResponse)
async def medicos(id: str):
    # bd.delete(id)
    return ""


@app.delete("/api/pacientes/{id}", response_class=HTMLResponse)
async def pacientes(id: str):
    return ""
