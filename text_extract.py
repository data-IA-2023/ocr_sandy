"""
=========================================
classe :
    extraction des information
methode :
    OCR_dict_to_BD (result_ocr, dict_BD) => return dict_BD
    OCR_main ( list_url ) => ajout les données dans la bd
=========================================
"""

# =========================================
# classe :
#     ocr
# methode :
#     OCR_image_to_dict => entée : lien d'une image, sortie : 2 dictionnaires
# =========================================
from ocr import OCR_image_to_dict

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
from req_bd import connect_bd, url_exist_to_bd, get_dict_to_bd

# =========================================
# importation :
# =========================================
import re

# =========================================
# classe et méthode :
# =========================================

def OCR_dict_to_BD (result_ocr, dict_BD) :
    """
    entrée : 2 dictionnaire, un de résultat, l'autre de l'api ocr
    sortie : un dictionnaire des données pour la base de données
    =====================================================================
    # >>> OCR_dict_to_BD(result_ocr=[{'text_line': 'INVOICE FAC_2019_0998', 'Confidence': 0.962}, {'text_line': 'Issue date 2019-12-18 18:21:00', 'Confidence': 0.9807}, {'text_line': 'Bill to Ivan Abate', 'Confidence': 0.98}, {'text_line': 'Brilllling', 'Confidence': 0.564}, {'text_line': 'Address Canale Adele, 2 Piano 8', 'Confidence': 0.9893}, {'text_line': '12053, Santuario Tinella (CN)', 'Confidence': 0.9918}, {'text_line': 'Eos reprehenderit cumque culpa.', 'Confidence': 0.9948}, {'text_line': '2 × 77.41 Euro', 'Confidence': 0.8882}, {'text_line': 'TOTAL', 'Confidence': 0.997}, {'text_line': '154.82 Euro', 'Confidence': 0.9925}])

    """
    
    if result_ocr == None :
        dict_BD['monitoring']['OCR_statut']= 'error in OCR_image_to_dict()'
        dict_BD['monitoring']['code_error_OCR']= 'le dictionnaire de résultat est vide'
        
    else :
        
        try :
            
            # teste par expretion réguliaire pour obtenir info
            for element in result_ocr :
                
                # print("element :", element)

                if element['Confidence'] > 0.8 :
                    text_element = element['text_line']

                    # test id_facture 
                    # regEx : 'INVOICE FAC_2019_0998'
                    pattern_1 = r"^INVOICE"
                    result_1 = re.match(pattern_1, text_element)
                    # print("result 1 :", result)
                    if result_1:
                        text_result = text_element[8:]
                        # print ("text_result :", text_result)
                        # print('id_facture trouvé')
                        dict_BD['facture']['id_facture']= text_result

                    # test date_facture 
                    # regEx : 'Issue date 2019-12-18 18:21:00'
                    pattern_2 = r"^Issue date"
                    result_2 = re.match(pattern_2, text_element)
                    # print("result 1 :", result)
                    if result_2:
                        text_result = text_element[10:-9]
                        # print ("text_result :", text_result)
                        # print('date_facture trouvé')
                        dict_BD['facture']['date_facture']= text_result

                    # test nom_client 
                    # regEx : 'Bill to Ivan Abate'
                    pattern_3 = r"^Bill to"
                    result_3 = re.match(pattern_3, text_element)
                    # print("result 1 :", result)
                    if result_3:
                        text_result = text_element[8:]
                        # print ("text_result :", text_result)
                        # print('nom_client trouvé')
                        dict_BD['client']['nom_client']= text_result

                    # test addesse_client 1
                    # regEx : 'Address Canale Adele, 2 Piano 8'
                    pattern_4 = r"^Address"
                    result_4 = re.match(pattern_4, text_element)
                    # print("result 1 :", result)
                    if result_4:
                        text_result = text_element[8:]
                        # print ("text_result :", text_result)
                        # print('addesse_client 1 trouvé')
                        dict_BD['client']['addesse_client']['1']= text_result

                    # test addesse_client 2 
                    # regEx : '12053, Santuario Tinella (CN)'
                    pattern_5 = r"^(\d){5}+,"
                    result_5 = re.match(pattern_5, text_element)
                    # print("result 1 :", result)
                    if result_5:
                        # print('addesse_client 2 trouvé')
                        dict_BD['client']['addesse_client']['2']= text_element

                    # test nom_produit
                    # regEx : 'Eos reprehenderit cumque culpa. 2 × 77.41 Euro'
                    # test prix_produit et quantite_produit
                    pattern_6 = r"(\d) +× (\d+).(\d+).Euro$"
                    result_6 = re.search(pattern_6, text_element)

                    if result_6:
                        # print("result 1 :", result)
                        position_num = result_6.start()

                        nom_result = text_element[:position_num]
                        produit_result = text_element[position_num:]
                        # print(f'nom_result-{nom_result}-')
                        # print(f'produit_result-{produit_result}-')

                        nom_produit = nom_result[:-2]
                        # print('nom_produit :', nom_produit)
                        
                        text_result = produit_result[:-5]
                        result_list = text_result.split("×")
                        # print ("text_result :", result_list)
                        quantite_produit_str = result_list[0][:-1]
                        quantite_produit = int(quantite_produit_str)
                        prix_produit_str = result_list[1][1:]
                        prix_produit = float(prix_produit_str)
                        # print(f'-{quantite_produit}-{prix_produit}-')

                        # print('nom_produit, prix_produit et quantite_produit trouvé')
                        dict_BD['produit'].append({'id_produit': nom_produit, 'nom_produit': nom_produit, 'prix_produit': prix_produit}) # ['prix_produit']= prix_produit
                        dict_BD['achat'].append({'id_produit': nom_produit, 'quantite_produit': quantite_produit})

                    # test total_facture
                    # regEx : '154.82 Euro'
                    pattern_7 = r"^(\d+)\.(\d+).Euro$"
                    pattern_8 = r"^TOTAL.(\d+)\.(\d+).Euro$"
                    result_7 = re.match(pattern_7, text_element) or re.match(pattern_8, text_element)
                    # print("result 2 :", result)
                    if result_7:
                        text_result = text_element[:-5]
                        text_result_2 = re.sub(r'[^0-9,]+', '', text_result)
                        # print ("text_result :", text_result)
                        # print('total_facture trouvé')
                        dict_BD['facture']['total_facture']= text_result_2
            
            dict_BD['monitoring']['OCR_statut']= f'success'
            # print("dict_BD in :", dict_BD)
            return dict_BD

        except Exception as e :
            dict_BD['monitoring']['OCR_statut']= 'error in OCR_dict_to_BD()'
            dict_BD['monitoring']['code_error_OCR']= e

# ==============================================================

def OCR_main ( list_url ) :
    # boucle pour tous les url de la liste :
    for url in list_url :

        print('url :', url, type(url))

        dict_bd_loop = { 'facture' : {'id_facture': None, 'image_facture': None, 'total_facture': None, 'date_facture': None},
                         'client': {'id_client': None, 'nom_client': None, 'addesse_client': {"1":None, "2":None}},
                         'produit': [],
                         'achat': [],
                         'monitoring': {'id_monitoring': None, 'OCR_statut': None, 'code_error_OCR': None,
                                        'BD_statut': None, 'code_error_BD': None}
            }
        
        try :
            conn = connect_bd()
            session = conn["session"]
            engine = conn["engine"]
            dict_bd_loop['monitoring']['BD_statut']= 'success'
        except Exception as e :
            dict_bd_loop['monitoring']['BD_statut']= 'error in OCR_dict_to_BD()'
            dict_bd_loop['monitoring']['code_error_BD']= e
            print('error in OCR_dict_to_BD()', e)
        
        if session :
            # teste si url déjà dans base de donnée :
            bool = url_exist_to_bd (url, session)

            if bool == True :
                print("l'url est déjà traité")
            else :
                ocr_dict, result_dict = OCR_image_to_dict(url, dict_bd_loop)

                # print("ocr_dict :", ocr_dict)
                # print("dict_bd :", dict_bd)

                # for element in ocr_dict :
                #     print("element :", element)

                to_BD_result = OCR_dict_to_BD (ocr_dict, result_dict)
                
                print ("to_BD_result :", to_BD_result)

                try :
                    get_dict_to_bd ( to_BD_result, session )
                except :
                    print("error dans l'ajout des données dans la bd")

# list = ["https://invoiceocrp3.azurewebsites.net/static/FAC_2019_1004-5124405.png",
#         "https://invoiceocrp3.azurewebsites.net/static/FAC_2019_0998-5758105.png"
#         ]
# list = ["https://invoiceocrp3.azurewebsites.net/static/FAC_2019_0005-1869518.png",
#         "https://invoiceocrp3.azurewebsites.net/static/FAC_2019_1004-5124405.png",
#         "https://invoiceocrp3.azurewebsites.net/static/FAC_2019_1024-9045.png",
#         "https://invoiceocrp3.azurewebsites.net/static/FAC_2019_1004-5124405.png",
#         "https://invoiceocrp3.azurewebsites.net/static/FAC_2019_0998-5758105.png"
#         ]
# r = OCR_main(list)

# print('r :', r)


"""
url : https://invoiceocrp3.azurewebsites.net/invoices/FAC_2019_0002-521208 <class 'str'>
to_BD_result : {'facture': {'id_facture': 'FAC_2019_0002', 'image_facture': 'https://invoiceocrp3.azurewebsites.net/invoices/FAC_2019_0002-521208', 'total_facture': 
'TOTAL 428.13', 'date_facture': ' 2019-01-01'}, 'client': {'id_client': None, 'nom_client': 'Sébastien Jean-Vasseur', 'addesse_client': {'1': '19246 Flowers Lake Suite 939', '2': None}}, 'produit': [], 'achat': [], 'monitoring': {'id_monitoring': None, 'OCR_statut': 'success', 'code_error_OCR': None, 'BD_statut': 'success', 'code_error_BD': None}}
adresse_dict : {'1': '19246 Flowers Lake Suite 939', '2': None}
id_client : 11
error dans l'ajout des données dans la bd
url : https://invoiceocrp3.azurewebsites.net/invoices/FAC_2019_0001-112650 <class 'str'>
to_BD_result : {'facture': {'id_facture': 'FAC_2019_0001', 'image_facture': 'https://invoiceocrp3.azurewebsites.net/invoices/FAC_2019_0001-112650', 'total_facture': 
'TOTAL 1472.19', 'date_facture': ' 2019-01-01'}, 'client': {'id_client': None, 'nom_client': 'Sarah Smith', 'addesse_client': {'1': '0496 Brianna Crossing', '2': None}}, 'produit': [], 'achat': [], 'monitoring': {'id_monitoring': None, 'OCR_statut': 'success', 'code_error_OCR': None, 'BD_statut': 'success', 'code_error_BD': None}}
adresse_dict : {'1': '0496 Brianna Crossing', '2': None}
id_client : 12
error dans l'ajout des données dans la bd
url : https://invoiceocrp3.azurewebsites.net/invoices/FAC_2019_0003-4174848 <class 'str'>
to_BD_result : {'facture': {'id_facture': 'FAC_2019_0003', 'image_facture': 'https://invoiceocrp3.azurewebsites.net/invoices/FAC_2019_0003-4174848', 'total_facture': 'TOTAL 323.73', 'date_facture': ' 2019-01-02'}, 'client': {'id_client': None, 'nom_client': 'Orlando Ovadia', 'addesse_client': {'1': '57, boulevard de Aubert', '2': None}}, 'produit': [{'id_produit': 'Accent discussion suivre lèvre', 'nom_produit': 'Accent discussion suivre lèvre', 'prix_produit': 59.23}], 'achat': [{'id_produit': 'Accent discussion suivre lèvre', 'quantite_produit': 1}], 'monitoring': {'id_monitoring': None, 'OCR_statut': 'success', 'code_error_OCR': None, 'BD_statut': 'success', 'code_error_BD': None}}
adresse_dict : {'1': '57, boulevard de Aubert', '2': None}
id_client : 13
error dans l'ajout des données dans la bd
url : https://invoiceocrp3.azurewebsites.net/invoices/FAC_2019_0004-46050 <class 'str'>
to_BD_result : {'facture': {'id_facture': 'FAC_2019_0004', 'image_facture': 'https://invoiceocrp3.azurewebsites.net/invoices/FAC_2019_0004-46050', 'total_facture': 'TOTAL 2853.88', 'date_facture': ' 2019-01-02'}, 'client': {'id_client': None, 'nom_client': 'Thibault Martinez de la Boucher', 'addesse_client': {'1': 'Strada Romolo, 8 Appartamento 62', '2': '35018, San Martino Di Lupari (PD)'}}, 'produit': [], 'achat': [], 'monitoring': {'id_monitoring': None, 'OCR_statut': 'success', 'code_error_OCR': None, 'BD_statut': 'success', 'code_error_BD': None}}
adresse_dict : {'1': 'Strada Romolo, 8 Appartamento 62', '2': '35018, San Martino Di Lupari (PD)'}
id_client : 14
error dans l'ajout des données dans la bd
url : https://invoiceocrp3.azurewebsites.net/invoices/FAC_2019_0006-6410304 <class 'str'>
to_BD_result : {'facture': {'id_facture': 'FAC_2019_0006', 'image_facture': 'https://invoiceocrp3.azurewebsites.net/invoices/FAC_2019_0006-6410304', 'total_facture': 'TOTAL 860.59', 'date_facture': ' 2019-01-03'}, 'client': {'id_client': None, 'nom_client': 'Courtney Washington', 'addesse_client': {'1': 'Viale Verga, 919 Appartamento 20', '2': '10045, Piossasco (TO)'}}, 'produit': [], 'achat': [], 'monitoring': {'id_monitoring': None, 'OCR_statut': 'success', 'code_error_OCR': None, 'BD_statut': 'success', 'code_error_BD': None}}
adresse_dict : {'1': 'Viale Verga, 919 Appartamento 20', '2': '10045, Piossasco (TO)'}
id_client : 15
error dans l'ajout des données dans la bd
url : https://invoiceocrp3.azurewebsites.net/invoices/FAC_2019_0005-1869518 <class 'str'>
to_BD_result : {'facture': {'id_facture': 'FAC_2019_0005', 'image_facture': 'https://invoiceocrp3.azurewebsites.net/invoices/FAC_2019_0005-1869518', 'total_facture': 'TOTAL 1647.47', 'date_facture': ' 2019-01-03'}, 'client': {'id_client': None, 'nom_client': 'Victoria Parker', 'addesse_client': {'1': 'USCGC Park', '2': None}}, 'produit': [], 'achat': [], 'monitoring': {'id_monitoring': None, 'OCR_statut': 'success', 'code_error_OCR': None, 'BD_statut': 'success', 'code_error_BD': None}}    
client_existe : <orm.Clients object at 0x0000020ABE5EDE80>
facture_existe : <orm.Factures object at 0x0000020ABE4E2DB0>
list_produits : [] list_achats : []
url : https://invoiceocrp3.azurewebsites.net/invoices/FAC_2019_0007-2747871 <class 'str'>
to_BD_result : {'facture': {'id_facture': 'FAC_2019_0007', 'image_facture': 'https://invoiceocrp3.azurewebsites.net/invoices/FAC_2019_0007-2747871', 'total_facture': 'TOTAL 345.81', 'date_facture': ' 2019-01-04'}, 'client': {'id_client': None, 'nom_client': 'Pierina Modiano', 'addesse_client': {'1': '170 Hopkins Dam', '2': None}}, 'produit': [], 'achat': [], 'monitoring': {'id_monitoring': None, 'OCR_statut': 'success', 'code_error_OCR': None, 'BD_statut': 'success', 'code_error_BD': None}}adresse_dict : {'1': '170 Hopkins Dam', '2': None}
id_client : 16
error dans l'ajout des données dans la bd
url : https://invoiceocrp3.azurewebsites.net/invoices/FAC_2019_0009-2407968 <class 'str'>
to_BD_result : {'facture': {'id_facture': 'FAC_2019_0009', 'image_facture': 'https://invoiceocrp3.azurewebsites.net/invoices/FAC_2019_0009-2407968', 'total_facture': 'TOTAL 2412.26', 'date_facture': ' 2019-01-04'}, 'client': {'id_client': None, 'nom_client': 'Anouk Pires', 'addesse_client': {'1': '82780 Jason Track', '2': None}}, 'produit': [], 'achat': [], 'monitoring': {'id_monitoring': None, 'OCR_statut': 'success', 'code_error_OCR': None, 'BD_statut': 'success', 'code_error_BD': None}} 
adresse_dict : {'1': '82780 Jason Track', '2': None}
id_client : 17
error dans l'ajout des données dans la bd
url : https://invoiceocrp3.azurewebsites.net/invoices/FAC_2019_0008-2031855 <class 'str'>
to_BD_result : {'facture': {'id_facture': 'FAC_2019_0008', 'image_facture': 'https://invoiceocrp3.azurewebsites.net/invoices/FAC_2019_0008-2031855', 'total_facture': 'TOTAL 1015.53', 'date_facture': ' 2019-01-04'}, 'client': {'id_client': None, 'nom_client': 'Maria Pacetti', 'addesse_client': {'1': '907, boulevard Sébastien Mathieu', '2': None}}, 'produit': [], 'achat': [], 'monitoring': {'id_monitoring': None, 'OCR_statut': 'success', 'code_error_OCR': None, 'BD_statut': 'success', 'code_error_BD': None}}
adresse_dict : {'1': '907, boulevard Sébastien Mathieu', '2': None}
id_client : 18
error dans l'ajout des données dans la bd
url : https://invoiceocrp3.azurewebsites.net/invoices/FAC_2019_0011-585056 <class 'str'>
to_BD_result : {'facture': {'id_facture': 'FAC_2019_0011', 'image_facture': 'https://invoiceocrp3.azurewebsites.net/invoices/FAC_2019_0011-585056', 'total_facture': 
'TOTAL 2382.83', 'date_facture': ' 2019-01-05'}, 'client': {'id_client': None, 'nom_client': 'Charles Guyot', 'addesse_client': {'1': '754 Larson Harbor', '2': None}}, 'produit': [], 'achat': [], 'monitoring': {'id_monitoring': None, 'OCR_statut': 'success', 'code_error_OCR': None, 'BD_statut': 'success', 'code_error_BD': None}}adresse_dict : {'1': '754 Larson Harbor', '2': None}
id_client : 19
error dans l'ajout des données dans la bd
url : https://invoiceocrp3.azurewebsites.net/invoices/FAC_2019_0010-5403720 <class 'str'>
to_BD_result : {'facture': {'id_facture': 'FAC_2019_0010', 'image_facture': 'https://invoiceocrp3.azurewebsites.net/invoices/FAC_2019_0010-5403720', 'total_facture': 'TOTAL 1070.64', 'date_facture': ' 2019-01-05'}, 'client': {'id_client': None, 'nom_client': 'Willie Aguirre', 'addesse_client': {'1': '5102 Joseph Valleys Apt. 283', '2': None}}, 'produit': [], 'achat': [], 'monitoring': {'id_monitoring': None, 'OCR_statut': 'success', 'code_error_OCR': None, 'BD_statut': 'success', 'code_error_BD': None}}
adresse_dict : {'1': '5102 Joseph Valleys Apt. 283', '2': None}
id_client : 20
"""