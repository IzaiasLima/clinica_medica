from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse

app = FastAPI()
app.mount("/app", StaticFiles(directory="static", html="True"), name="static")


@app.get("/", response_class=RedirectResponse)
async def root():
    return "/app/login.html"


@app.get("/api", response_class=RedirectResponse)
async def root():
    return "/app/login.html"


@app.get("/api/pacientes")
async def pacientes():
    return get_pacientes()


@app.get("/api/medicos")
async def medicos():
    dados = get_medicos()
    return dados


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
            "email": "ciane@gmail.COM",
            "especialidade": "dermatologia",
            "turno": "diurno",
            "status": "em análise",
        },
        {
            "nome": "luciana monteiro",
            "crm": "4445566",
            "email": "DRA@LUCIANA.COM",
            "especialidade": "dermatologia",
            "turno": "noturno",
            "status": "ativo",
        },
        {
            "nome": "NATANAEL MONTEIRO",
            "crm": "556688",
            "email": "Natan@email.com",
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
            "telefone": "61 98181-3390",
            "status": "internado",
        },
        {
            "nome": "Kaio de Oliveira",
            "email": "KAIO@gmail.com.BR",
            "telefone": "61 98182-3393",
            "status": "em atendimento",
        },
        {
            "nome": "Izaias lima",
            "email": "izaias@gmail.com",
            "status": "atendido",
            "telefone": "61 98180-3090",
        },
    ]
    return dados


@app.delete("/api/medicos/{id}", response_class=HTMLResponse)
async def medicos(id: str):
    return ""


@app.delete("/api/pacientes/{id}", response_class=HTMLResponse)
async def pacientes(id: str):
    return ""
