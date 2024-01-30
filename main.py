from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/app", StaticFiles(directory="static", html="True"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=RedirectResponse)
async def root():
    return "/app/login.html"


@app.get("/api", response_class=RedirectResponse)
async def root():
    return "/app/login.html"


@app.get("/api/pacientes")
async def pacientes():
    return get_pacientes()


@app.get("/api/medicos", response_class=HTMLResponse)
async def medicos(request: Request):
    medicos = get_medicos()
    dados_html = templates.TemplateResponse(
        "tpl_medicos.html", {"request": request, "dados": medicos}
    )

    return dados_html


def get_medicos():
    dados = [
        {
            "nome": "Kaio de Oliveira",
            "crm": "123456",
            "email": "kaio@gmail.com",
            "especialidade": "cardiologia",
            "turno": "noturno",
            "status": "ativo",
        },
        {
            "nome": "Dileyciane Monteiro",
            "crm": "23456",
            "email": "",
            "especialidade": "dermatologia",
            "turno": "diurno",
            "status": "em análise",
        },
        {
            "nome": "luciana monteiro",
            "crm": "4445566",
            "email": "",
            "especialidade": "dermatologia",
            "turno": "noturno",
            "status": "ativo",
        },
        {
            "nome": "NATANAEL MONTEIRO",
            "crm": "556688",
            "email": "",
            "especialidade": "CARDIOLOGIA",
            "turno": "VESPERTINO",
            "status": "ATIVO",
        },
    ]

    return dados


def get_pacientes():
    dados = [
        {
            "nome": "Natanael Monteiro",
            "email": "natan@gmail.com",
            "status": "internado",
        },
        {
            "nome": "Kaio de Oliveira",
            "email": "kaio@gmail.com",
            "status": "em atendimento",
        },
        {
            "nome": "Izaias Lima",
            "email": "izaias@gmail.com",
            "status": "atendido",
        },
    ]
    return dados


@app.delete("/api/medicos/{id}", response_class=HTMLResponse)
async def medicos(id: str):
    return ""


@app.delete("/api/pacientes/{id}", response_class=HTMLResponse)
async def pacientes(id: str):
    return ""
