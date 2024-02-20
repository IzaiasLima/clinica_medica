from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse

import json
import urllib.parse as html

import db
import db_init
import static.fragments.html_edit as edit


app = FastAPI(
    title="Clinica Médica",
    version="0.0.1",
    summary="Protótipo de uma API para gestão de uma clínica médica. ",
)

app.mount("/app", StaticFiles(directory="static", html="True"), name="static")


async def get_body(req: Request):
    payload = await req.body()
    payload = payload.decode("utf8")
    payload = html.unquote(payload)

    try:
        body = json.loads(payload)
    except:
        lista = list(payload.split("&"))
        body = dict(l.split("=") for l in lista)

    return body


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


@app.get("/api/pacientes/{id}")
async def paciente(id):
    dados = db.get_paciente(id)
    return JSONResponse(dados)


@app.put("/api/pacientes/{id}", response_class=JSONResponse)
async def update_paciente(id, body=Depends(get_body)):
    db.update_paciente(id, body)
    dados = db.get_pacientes()
    return dados


@app.delete("/api/pacientes/{id}", response_class=HTMLResponse)
async def del_paciente(id: str):
    db.del_paciente(id)
    return ""


@app.get("/api/medicos", response_class=JSONResponse)
async def medicos():
    return db.get_medicos()


@app.delete("/api/medicos/{id}", response_class=HTMLResponse)
async def del_medico(id: str):
    db.del_medico(id)
    return ""


# resetar o banco de dados
@app.get("/reset", response_class=RedirectResponse)
def db_reset():
    db_init.tables_init()
    return "/app/home.html"


# retornar template para editar paciente
@app.get("/api/pacientes/{id}/edit", response_class=HTMLResponse)
async def edit_paciente(id):
    paciente = db.get_paciente(id)

    if paciente:
        dados = paciente[0]
        return edit.paciente_html(dados)
    else:
        raise HTTPException(status_code=404, detail="Item not found")
