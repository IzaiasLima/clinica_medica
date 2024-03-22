from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, RedirectResponse, HTMLResponse

import json

import time
import urllib.parse as html

import db

# import static.fragments.html_add as add
# import static.fragments.html_edit as edit

# import static.fragments.fragment as fragment

ERR_MSG = "Todos os campos precisam ser preenchidos!"

app = FastAPI(
    title="Clinica Médica",
    version="0.1.1",
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


@app.get("/api/capitulo", response_class=JSONResponse)
async def root():
    return {"capitulo": sort_chapter()}


@app.get("/api/pacientes", response_class=JSONResponse)
async def pacientes():
    dados = db.get_pacientes()
    return dados


@app.get("/api/pacientes/{id}", response_class=JSONResponse)
async def paciente(id: int):
    dados = db.get_paciente(id)
    return dados


@app.post("/api/pacientes", response_class=JSONResponse)
async def add_paciente(body=Depends(get_body)):
    if is_valid(body, 5):
        db.add_paciente(body)
        dados = db.get_pacientes()
        return dados
    else:
        raise HTTPException(status_code=422, detail=ERR_MSG)


@app.put("/api/pacientes/{id}", response_class=JSONResponse)
async def update_paciente(id: int, body=Depends(get_body)):
    if is_valid(body, 6):
        db.update_paciente(id, body)
        dados = db.get_pacientes()
        return dados
    else:
        raise HTTPException(status_code=422, detail=ERR_MSG)


@app.delete("/api/pacientes/{id}", response_class=HTMLResponse)
async def del_paciente(id: int):
    db.del_paciente(id)
    return ""


@app.get("/api/medicos", response_class=JSONResponse)
async def medicos():
    return db.get_medicos()


@app.get("/api/medicos/{id}", response_class=JSONResponse)
async def medico(id: int):
    return db.get_medico(id)


@app.post("/api/medicos", response_class=JSONResponse)
async def add_medico(body=Depends(get_body)):
    if is_valid(body, 8):
        db.add_medico(body)
        dados = db.get_medicos()
        return dados
    else:
        raise HTTPException(status_code=422, detail=ERR_MSG)


@app.post("/api/medicos/search", response_class=JSONResponse)
async def get_medicos(body=Depends(get_body)):
    time.sleep(0.5)
    busca = body["search"]
    dados = db.get_medicos() if len(busca) < 2 else db.search_medicos(busca)
    return dados


@app.put("/api/medicos/{id}", response_class=JSONResponse)
async def update_medico(id: int, body=Depends(get_body)):
    if is_valid(body, 9):
        db.update_medico(id, body)
        return db.get_medicos()
    else:
        raise HTTPException(status_code=422, detail=ERR_MSG)


@app.delete("/api/medicos/{id}")
async def del_medico(id: int):
    db.del_medico(id)
    return HTMLResponse(status_code=200)


# -------------------------------------- #


# retornar template para incluir paciente
@app.get("/api/pacientes/new/add", response_class=HTMLResponse)
async def add_paciente():
    html = fragment("paciente_add")
    return "".join(html)


# retornar template para editar paciente
@app.get("/api/pacientes/{id}/edit", response_class=HTMLResponse)
async def edit_paciente(id: int):
    dados = db.get_paciente(id)

    if dados:
        paciente = dados[0]
        html = "".join(fragment("paciente_edit"))
        html = html.format(**paciente)
        return html
    else:
        raise HTTPException(status_code=404)


# retornar template para incluir medico
@app.get("/api/medicos/new/add", response_class=HTMLResponse)
async def add_medico():
    html = fragment("medico_add")
    return "".join(html)


# retornar template para editar medico
@app.get("/api/medicos/{id}/edit", response_class=HTMLResponse)
async def edit_medico(id: int):
    dados = db.get_medico(id)

    if dados:
        medico = dados[0]
        html = "".join(fragment("medico_edit"))
        html = html.format(**medico)
        return html
    else:
        raise HTTPException(status_code=404)


# --------------------------------------- #


# resetar o banco de dados
@app.get("/reset", response_class=RedirectResponse)
def db_reset():
    import db_init

    db_init.tables_init()
    return "/app/home.html"


def is_valid(body: dict, qtd: int):
    fields = sum([1 if v else 0 for _, v in body.items()])
    return fields == qtd


def fragment(frag):
    html = open(f"./static/fragments/{frag}.html", "r").readlines()
    return "".join(html)


def sort_chapter():
    import random as r

    chapter = [1, 2, 14, 15, 23, 24, 91, 100, 133, 150][r.randint(0, 9)]
    return chapter
