from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import random
# import dotenv, os

# =========================================
# run : uvicorn main:app
# =========================================

# dotenv.load_dotenv()
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/statics", StaticFiles(directory="statics"), name="statics")

@app.get("/")
def get_home(request: Request):
    return templates.TemplateResponse( request=request, name="home.html", context={} )

@app.get("/home")
def get_home(request: Request):
    return templates.TemplateResponse( request=request, name="home.html", context={} )

@app.get("/ocr")
def get_ocr(request: Request):
    return templates.TemplateResponse( request=request, name="ocr.html", context={} )

@app.get("/compta")
def get_compta(request: Request):
    return templates.TemplateResponse( request=request, name="compta.html", context={} )

@app.get("/monit")
def get_monit(request: Request):
    return templates.TemplateResponse( request=request, name="monit.html", context={} )