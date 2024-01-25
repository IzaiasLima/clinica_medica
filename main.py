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
