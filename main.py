from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse

app = FastAPI()
app.mount("/app", StaticFiles(directory="static", html="True"), name="static")


@app.get("/", response_class=RedirectResponse)
async def root():
    return "/app/login.html"


@app.get("/api", response_class=HTMLResponse)
async def api():
    return """
        <!DOCTYPE html>
        <html>
        <head>
            <meta http-equiv="refresh" content="0; URL='./app/login.html'">
        </head>
        </html>
    """


@app.get("/api/medicos")
async def medicos():
    return get_medicos()


def get_medicos():
    dados = {
        "nome": "Kaio Oliveira",
        "crm": "123456",
        "especialidade": "cardiologia",
        "turno": "noturno",
        "status": "ativo",
    }

    return dados


"""
    Nome	CRM	Especialidade	Turno	Situação	 
    Dileyciane Monteiro	234567	Dermatologia	Diurno	Em análise	 
    Naelle Monteiro	345678	Pediatria	Diurno	Ativo	 
    Lidia Monteiro	456789	Nutrição	Vespertino	Inativo	 
"""
