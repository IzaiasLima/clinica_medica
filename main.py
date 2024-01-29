from fastapi import FastAPI
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


@app.get("/api/medicos", response_class=HTMLResponse)
async def medicos():
    dados_html = """
    <table>
        <thead>
            <tr>
                <th>Nome</th>
                <th>CRM</th>
                <th>Especialidade</th>
                <th>Turno</th>
                <th>Situação</th>
                <th colspan="2">&nbsp;</th>
            </tr>
        </thead>

        <tbody>
            <tr>
                <td>Kaio Oliveira</td>
                <td>123456</td>
                <td>Cardiologia</td>
                <td>Noturno</td>
                <td>Ativo</td>
                <td>
                    <i class="fa fa-pencil"></i>
                </td>
                <td>
                    <i class="fa fa-trash-o"></i>
                </td>
            </tr>
        </tbody>
    </table>
    """

    return dados_html


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
