"""
=========================================
classe :
    get_facture
methode :
    get_all_facture_url () => return listr de tous les url
    get_nb_facture_url (date, nb) => return listr de nb url (date au forma datetime)
=========================================
"""

# =========================================
# imprtation :
# =========================================
import requests, json
import pandas as pd
import datetime, os

# =========================================
# classe et méthode :
# =========================================

# Trouve le chemein du fichier .env et l'ouvre par dotenv
repertoir_fichier = os.path.dirname(__file__)
# print(repertoir_fichier)
facture_path = f'{repertoir_fichier}\\statics\\list_requests.json'

# ==================== télécharger une facture forma png à partir d'un no ====================
def get_une_facture (no) :
    """
    entrée : no de type FAC_20xx_xxxx-xxxxxxx
    sorti : fichier png
    """
    url_base = "https://invoiceocrp3.azurewebsites.net/invoices/"
    url_spe = f"{no}"
    url = f'{url_base}{url_spe}'
    r = requests.get(url, allow_redirects=True)

    # print(r.content)
    open(f'statics/factures/{no}.png', 'wb').write(r.content)

# get_une_facture("FAC_2019_0998-5758105")

# ==================== télécharger plusieur factures forma png à partir d'un no ====================
def telechargement ():
    # ouvrir json, liste des facture
    with open('statics/list_requests.json','r') as json_File :
        sample_load_file=json.load(json_File)
        list_facture = sample_load_file['invoices']
        print("list_facture :", list_facture)

        # pour chaque facture => no et dt + telecharge
        # return dt 
        count = 0 # limite de facture à télécharger
        while count < 1000 :
            for element in list_facture :
                no_element = element['no']
                dt_element = element['dt']
                print("no_element :", no_element, "dt_element :", dt_element)
                get_une_facture(no_element)
                count += 1
    
    return dt_element

# ==================== genere liste de lien url factures ====================
def get_all_facture_url () :
    list_url = []
    with open('statics/list_requests.json','r') as json_File :
        sample_load_file=json.load(json_File)
        list_facture = sample_load_file['invoices']
        # print("list_facture :", list_facture)

        for element in list_facture :
            # print("element :", element)
            # print(element['no'])
            list_url.append(f"https://invoiceocrp3.azurewebsites.net/invoices/{element['no']}")

        # print("list_url :", list_url)

        return list_url

# get_all_facture_url()

def get_nb_facture_url (date, nb) :
        
    list_url = []
    with open('statics/list_requests.json','r') as json_File :
        sample_load_file=json.load(json_File)
        list_facture = sample_load_file['invoices']
        # print("list_facture :", list_facture)

        get_url = False
        count = 0
        for element in list_facture :
            # print("element :", element)
            # print(element['dt'])
            # print(date)
            date_element = datetime.datetime.strptime(element['dt'], '%Y-%m-%d %H:%M:%S')
            if date_element >= date and count < nb:
                get_url = True
                list_url.append(f"https://invoiceocrp3.azurewebsites.net/invoices/{element['no']}")
                count += 1
                # print(get_url)
            if count == nb :
                break
            # print(count)

        return list_url

# d1, m1, y1 = f'17/12/2020'.split('/')
# print(d1, m1, y1)
# date = datetime.datetime( day=int(d1), month=int(m1), year=int(y1) )
# print(date)
# list_url = get_nb_facture_url(date, 10)
# print(list_url)