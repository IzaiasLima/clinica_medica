from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import (
    JSONResponse,
    RedirectResponse,
    HTMLResponse,
    PlainTextResponse,
)

import json

import time
import urllib.parse as html

import db


ERR_MSG = "Todos os campos precisam ser preenchidos!"
LEN_PAGE = 5

app = FastAPI(
    title="Clínica Mentalis",
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

    body.pop("page", None)
    return body


async def get_params(req: Request):
    payload = req.query_params

    try:
        params = dict(payload)
    except:
        params = None

    return params


@app.get("/", response_class=RedirectResponse)
async def root():
    return "/app/login.html"


@app.get("/info/title", response_class=PlainTextResponse)
def get_info():
    return app.title


@app.get("/api", response_class=RedirectResponse)
async def api_root():
    return "/app/login.html"


@app.get("/api/capitulo", response_class=JSONResponse)
async def capitulo():
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


@app.post("/api/pacientes/search", response_class=JSONResponse)
async def search_pacientes(body=Depends(get_body)):
    search = body["search"]
    dados = db.get_pacientes() if len(search) < 2 else db.search_pacientes(search)
    return dados


@app.put("/api/pacientes/{id}", response_class=JSONResponse)
async def update_paciente(id: int, body=Depends(get_body)):
    if is_valid(body, 6):
        db.update_paciente(id, body)
        dados = db.get_paciente(id)
        # dados = db.get_pacientes()
        # dados = db.get_medicos_paged(LEN_PAGE)
        return dados
    else:
        raise HTTPException(status_code=422, detail=ERR_MSG)


@app.delete("/api/pacientes/{id}", response_class=HTMLResponse)
async def del_paciente(id: int):
    db.del_paciente(id)
    return ""


@app.get("/api/medicos", response_class=JSONResponse)
async def medicos(params=Depends(get_params)):
    if params:
        page = int(params["page"])
        page = 0 if page < 0 else page
        dados = db.get_medicos_paged(LEN_PAGE, page)
        dados.update(pagination("medicos", page))
        return dados
    else:
        return db.get_medicos()


@app.get("/api/medicos/{id}", response_class=JSONResponse)
async def medico(id: int):
    return db.get_medico(id)


@app.post("/api/medicos", response_class=JSONResponse)
async def add_medico(body=Depends(get_body)):
    if is_valid(body, 11):
        db.add_medico(body)
        dados = db.get_medicos_paged(LEN_PAGE)
        dados.update(pagination("medicos"))
        return dados
    else:
        raise HTTPException(status_code=422, detail=ERR_MSG)


@app.post("/api/medicos/search", response_class=JSONResponse)
async def search_medicos(body=Depends(get_body)):
    search = body["search"]
    dados = None

    if len(search) < 2:
        dados = db.get_medicos_paged(LEN_PAGE)
        dados.update(pagination("medicos"))
    else:
        dados = db.search_medicos(search)
        # dados.update(pagination())

    return dados


@app.put("/api/medicos/{id}", response_class=JSONResponse)
async def update_medico(id: int, body=Depends(get_body)):
    try:
        page_number = int(body["page_number"])
        body.pop("page_number", None)
    except:
        page_number = 0

    if is_valid(body, 10):
        db.update_medico(id, body)
        dados = db.get_medicos_paged(LEN_PAGE, page_number)
        dados.update(pagination("medicos", page_number))
        # dados = db.get_medico(id)
        return dados
    else:
        raise HTTPException(status_code=422, detail=ERR_MSG)


@app.delete("/api/medicos/{id}")
async def del_medico(id: int):
    db.del_medico(id)
    return HTMLResponse(status_code=200)


# -------------------------------------- #
#       RETORNA FRAGMENTOS DE HTML       #
# -------------------------------------- #


# retornar template para incluir paciente
@app.get("/html/pacientes/new/add", response_class=HTMLResponse)
async def add_paciente():
    html = fragment("paciente_add")
    return "".join(html)


# retornar template para editar paciente
@app.get("/html/pacientes/{id}/edit", response_class=HTMLResponse)
async def edit_paciente(id: int):
    dados = db.get_paciente(id)
    return fragment_format(dados, "paciente_edit")


# retornar template para exibir detalhes do paciente
@app.get("/html/pacientes/{id}/detalhe", response_class=HTMLResponse)
async def detalhe_paciente(id: int):
    dados = db.get_paciente(id)
    return fragment_format(dados, "paciente_detalhes")


# retornar template para incluir medico
@app.get("/html/medicos/new/add", response_class=HTMLResponse)
async def add_medico():
    html = fragment("medico_add")
    return html


# retornar template para editar medico
@app.get("/html/medicos/{id}/edit", response_class=HTMLResponse)
async def edit_medico(id: int, params=Depends(get_params)):
    page = params["page"] if params else 0
    dados = db.get_medico(id)
    html = fragment_format(dados, page, "medico_edit")
    return html


# retornar template para exibir detalhes do paciente
@app.get("/html/medicos/{id}/detalhe", response_class=HTMLResponse)
async def detalhe_medico(id: int):
    dados = db.get_medico(id)
    return fragment_format(dados, "medico_detalhes")


# retorna um fragmento com o menu do sistema #
@app.get("/html/menu", response_class=HTMLResponse)
def get_menu():
    html = fragment("menu")
    return html


# --------------------------------------- #
# FUNÇÕES AUXILIARES E ENDPOINTS DE TESTE #
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


def fragment_format(dados, page, frag):
    if dados:
        page_number = f"'page_number': {page}"
        html = fragment(frag)
        html = html.format(
            page_number=page_number,
            **dados[0],
        )
        return html
    else:
        raise HTTPException(status_code=404)


def pagination(tbl, page=0):
    total_pages = (db.count(tbl) - 1) // LEN_PAGE

    pages = {}

    if total_pages > 0:
        pages = {
            "pagination": {
                "first_page": page == 0,
                "alias_first_page": "first_page" if page == 0 else "",
                "previous_page": page - 1 if page > 1 else 0,
                "page": page,
                "next_page": page + 1 if page < total_pages else page,
                "alias_last_page": "last_page" if page >= total_pages else "",
                "last_page": page >= total_pages,
                "total_pages": total_pages,
            }
        }
    return pages


def sort_chapter():
    import random as r

    chapter = [1, 2, 14, 15, 23, 24, 91, 100, 133, 150][r.randint(0, 9)]
    return chapter
