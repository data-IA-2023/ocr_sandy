"""
=========================================
classe :
    main
methode :
    "/ocr_few"
    "/ocr_all"
page html :
    "/ocr"
    "/compta"
    "/monit"
=========================================
"""

# =========================================
# classe :
#     get_facture
# methode :
#     get_all_facture_url () => return listr de tous les url
#     get_nb_facture_url (date, nb) => return listr de nb url (date au forma datetime)
# =========================================
from get_facture import get_nb_facture_url, get_all_facture_url

# =========================================
# classe :
#     extraction des information
# methode :
#     OCR_dict_to_BD (result_ocr, dict_BD) => return dict_BD
#     OCR_main ( list_url ) => ajout les données dans la bd
# =========================================
from text_extract import OCR_main

# =========================================
# classe :
#     traitement des requettes de la base de données
# methode :
#     def connect_bd () => return dict = { "session" : session, "engine" : engine }
#     url_exist_to_bd ( url, session) => return true ou false
#     get_dict_to_bd (dict, session )
#     get_df_stat (session, engine) => return dict = {'df_facture':df_facture, 'df_client':df_client, 'df_produit':df_produit, 'df_achat':df_achat}
#     get_df_monitoring (session, engine) return data frame of monitoring class
# =========================================
from req_bd import connect_bd, get_df_stat, get_df_monitoring


from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import datetime
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

@app.post("/ocr_few")
def get_ocr(request: Request, nombre: str = Form(), times: str = Form(), action: str = Form()):
    d1, m1, y1 = times.split('/')
    date = datetime.datetime( day=int(d1), month=int(m1), year=int(y1) )
    print(date)
    list_url = get_nb_facture_url (date, nombre)
    try :
        OCR_main (list_url)
        resultat = True
    except Exception as e :
        resultat = e
    return templates.TemplateResponse( request=request, name="ocr.html", context={"resultat":resultat} )

@app.post("/ocr_all")
def get_ocr(request: Request):
    list_url = get_all_facture_url ()
    try :
        OCR_main (list_url)
        resultat = True
    except Exception as e :
        resultat = e
    return templates.TemplateResponse( request=request, name="ocr.html", context={"resultat":resultat} )

@app.get("/compta")
def get_compta(request: Request):
    try :
        conn = connect_bd()
        session = conn["session"]
        engine = conn["engine"]

        resultat = get_df_stat(session, engine)
        df_facture = resultat['df_facture']
        df_client = resultat['df_client']
        df_produit = resultat['df_produit']
        df_achat = resultat['df_achat']
    except Exception as e :
        resultat_error = e

    return templates.TemplateResponse( request=request, name="compta.html", context={'df_facture':df_facture, 'df_client':df_client, 'df_produit':df_produit, 'df_achat':df_achat, "resultat_error":resultat_error} )

@app.get("/monit")
def get_monit(request: Request):
    try :
        conn = connect_bd()
        session = conn["session"]
        engine = conn["engine"]

        resultat = get_df_monitoring(session, engine)
    except Exception as e :
        resultat = e

    print("resultat :", resultat)
    return templates.TemplateResponse( request=request, name="monit.html", context={"resultat":resultat} )

# ==================== pour remplire la base de données ====================
list_url_all = get_all_facture_url ()
print(len(list_url_all))
# print(list_url_all, type(list_url_all))
# OCR_main (list_url_all)

d1, m1, y1 = f'19/10/2021'.split('/')
print(d1, m1, y1)
date = datetime.datetime( day=int(d1), month=int(m1), year=int(y1) )
list_url = get_nb_facture_url (date, 1000)
print(list_url, type(list_url))
OCR_main (list_url)