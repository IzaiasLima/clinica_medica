from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse

import db
import db_init

app = FastAPI(
    title="Clinica Médica",
    version="0.0.1",
    summary="Proposta de desenvolvimento de uma API para gestão de uma clínica médica. ",
)

app.mount("/app", StaticFiles(directory="static", html="True"), name="static")


@app.get("/", response_class=RedirectResponse)
async def root():
    return "/app/login.html"


@app.get("/api", response_class=RedirectResponse)
async def root():
    return "/app/login.html"


@app.get("/api/pacientes")
async def pacientes():
    dados = db.get_pacientes()
    return JSONResponse(dados)


@app.get("/api/medicos", response_class=JSONResponse)
async def medicos():
    return db.get_medicos()


@app.delete("/api/medicos/{id}", response_class=HTMLResponse)
async def del_medico(id: str):
    db.del_medico(id)
    return ""


@app.delete("/api/pacientes/{id}", response_class=HTMLResponse)
async def del_paciente(id: str):
    db.del_paciente(id)
    return ""


@app.get("/reset", response_class=RedirectResponse)
def db_reset():
    db_init.tables_init()
    return "/app/home.html"
