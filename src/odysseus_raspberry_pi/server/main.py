from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from odysseus_raspberry_pi.server.camera.router import router as camera_router
from odysseus_raspberry_pi.server.power.router import router as power_router

BASE_DIR = Path(__file__).resolve().parent

# Application instance
app = FastAPI()

# HTML template for the views
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# Where to fetch the static files for the views
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

app.include_router(camera_router)
app.include_router(power_router)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.get("/manual_drive", response_class=HTMLResponse)
async def manual_drive(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="manual_drive_view.html",
        context={}
    )