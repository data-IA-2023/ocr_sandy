"""
=========================================
classe :
    get_facture
methode :

=========================================
"""

# =========================================
# imprtation :
# =========================================
import requests, json

# =========================================
# classe et méthode :
# =========================================

def get_une_facture (no) :
    """
    entrée : no de type FAC_20xx_xxxx-xxxxxxx
    sorti : fichier png
    ===============================================

    """
    url_base = "https://invoiceocrp3.azurewebsites.net/invoices/"
    url_spe = f"{no}"
    url = f'{url_base}{url_spe}'
    r = requests.get(url, allow_redirects=True)

    # print(r.content)
    open(f'statics/factures/{no}.png', 'wb').write(r.content)

# get_une_facture("FAC_2019_0998-5758105")


def get_facture_no_start_years () :
    url_list_req ="https://invoiceocrp3.azurewebsites.net/invoices?"
    header = { "accept": "application/json" }
    r = requests.get(url_list_req, allow_redirects=True, headers=header)

    # print(r.content)
    open(f'list_requests.json', 'wb').write(r.content)

    # ouvrir json, liste des facture

    # pour chaque facture => no et dt + telecharge
    # return dt 


def get_facture_start_years (date) :
    url_list_req = f"https://invoiceocrp3.azurewebsites.net/invoices?start_date={date}"

    header = { "accept": "application/json" }
    r = requests.get(url_list_req, allow_redirects=True, headers=header)

    # print(r.content)
    open(f'statics/list_requests.json', 'wb').write(r.content)

    # ouvrir json, liste des facture
    with open('statics/list_requests.json','r') as json_File :
        sample_load_file=json.load(json_File)
        list_facture = sample_load_file['invoices']
        print("list_facture :", list_facture)

        # pour chaque facture => no et dt + telecharge
        # return dt 
        for element in list_facture :
            no_element = element['no']
            dt_element = element['dt']
            print("no_element :", no_element, "dt_element :", dt_element)
            get_une_facture(no_element)
    
    return dt_element


# dt_final = get_facture_start_years ("2019-12-18%2009%3A28%3A00")
# print("dt_final :", dt_final)

# def get_tous_facture () :

# requette url :
# https://invoiceocrp3.azurewebsites.net/invoices?start_date=2019-12-18%2009%3A28%3A00

# obtien un json avec liste de 1000 facture 
#     {
#       "no": "FAC_20xx_xxxx-xxxxxxx",
#       "dt": "20xx-xx-xx xx:xx:xx"
#     }

# boucle pour chaque facture :
#     requette url :
#     https://invoiceocrp3.azurewebsites.net/invoices/FAC_20xx_xxxx-xxxxxxx
#     telecharge png du fichier ou pdf

# quand fini, boucle pour les 1000 factures suivante avec "start_date=" le dernier "dt"