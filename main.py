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


@app.get("/api/medicos", response_class=HTMLResponse)
async def medicos(request: Request):
    medicos = get_medicos()
    dados_html = templates.TemplateResponse(
        "tpl_medicos.html", {"request": request, "dados": medicos}
    )

    return dados_html


# @app.get("/api/medicos", response_class=HTMLResponse)
# async def medicos():
#     dados_html = """
#     <table>
#         <thead>
#             <tr>
#                 <th>Nome</th>
#                 <th>CRM</th>
#                 <th>Especialidade</th>
#                 <th>Turno</th>
#                 <th>Situação</th>
#                 <th colspan="2">&nbsp;</th>
#             </tr>
#         </thead>

#         <tbody>
#             <tr>
#                 <td>Kaio Oliveira</td>
#                 <td>123456</td>
#                 <td>Cardiologia</td>
#                 <td>Noturno</td>
#                 <td>Ativo</td>
#                 <td>
#                     <i class="fa fa-pencil"></i>
#                 </td>
#                 <td>
#                     <i class="fa fa-trash-o"></i>
#                 </td>
#             </tr>
#         </tbody>
#     </table>
#     """

#     return dados_html


def get_medicos():
    dados = [
        {
            "nome": "Kaio Oliveira",
            "crm": "123456",
            "especialidade": "cardiologia",
            "turno": "noturno",
            "status": "ativo",
        },
        {
            "nome": "Dileyciane Monteiro",
            "crm": "23456",
            "especialidade": "dermatologia",
            "turno": "diurno",
            "status": "em análise",
        },
        {
            "nome": "Luciana Monteiro",
            "crm": "4445566",
            "especialidade": "dermatologia",
            "turno": "noturno",
            "status": "ativo",
        },
    ]

    return dados


"""
    Nome	CRM	Especialidade	Turno	Situação	 
    Naelle Monteiro	345678	Pediatria	Diurno	Ativo	 
    Lidia Monteiro	456789	Nutrição	Vespertino	Inativo	 
"""
