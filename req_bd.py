"""
=========================================
classe :
    traitement des requettes de la base de données
methode :
    def connect_bd () => return dict = { "session" : session, "engine" : engine }
    url_exist_to_bd ( url, session) => return true ou false
    get_dict_to_bd (dict, session )
    get_df_stat (session, engine) => return dict = {'df_facture':df_facture, 'df_client':df_client, 'df_produit':df_produit, 'df_achat':df_achat}
    get_df_monitoring (session, engine) return data frame of monitoring class
=========================================
"""

# =========================================
# classe :
#     orm
# methode :
#     connectBd 
#     createsession
# =========================================
# classe :
#     Factures
# attribus :
#     idFacture
#     imagePath
#     idClient
#     total
#     dateFacture
# =========================================
# classe :
#     Clients
# attribus :
#     idClient
#     nomClient 
#     adresse
# =========================================
# classe :
#     Produits
# attribus :
#     idProduit
#     nomProduit
#     prix
# =========================================
# classe :
#     Achats
# attribus :
#     idAchat
#     idFacture
#     idProduit
#     quantites
# =========================================
# classe :
#     Monitoring
# attribus :
#     idMonitoring
#     ocrStatut
#     codeErrorOCR
#     bdStatut
#     codeErrorBD
#     idFacture
#     dateMonitoring
# =========================================
import orm 

# =========================================
# importation :
# =========================================
import datetime
import pandas as pd

# ========================================
# methode pour connection et faire la session de la bd
# ========================================
def connect_bd () :
    # connection a la base de donnee
    engine = orm.connectBd()

    # creation de la session
    session = orm.createsession(engine)

    return { "session" : session, "engine" : engine }

# ========================================
# methode pour tester existence d'une url dans la bd
# ========================================
def url_exist_to_bd ( url, session) :
    url_existe = session.query(orm.Factures).filter_by(imagePath = url).first()
    
    if url_existe :
        return True
    else:
        return False

# existing_invoice = session.query(Facture).filter_by(QRid=data['QRid']).first()

# methode pour ajouter des données dans la bd
# dictionnaire structure :
# dict_bd = { 'facture' : {'id_facture': None, 'image_facture': None, 'total_facture': None, 
#                          'date_facture': None},
#            'client': {'id_client': None, 'nom_client': None, 'addesse_client': {"1":None, "2":None}},
#            'produit': [{'id_produit': nom_produit, 'nom_produit': None, 'prix_produit': None}],
#            'achat': [{'id_produit': nom_produit, 'quantite_produit': None}],
#            'monitoring': {'id_monitoring': None, 'OCR_statut': None, 'code_error_OCR': None,
#                           'BD_statut': None, 'code_error_BD': None}
#             }

# ========================================
# methode pour ajouter élément d'une facture à une base de données
# ========================================
def get_dict_to_bd (dict_fact, session) :

    # ========== traitement du client ==========

    # Vérification si la facture existe déjà dans la base de données
    try :
        client_existe = session.query(orm.Clients).filter_by(nomClient=dict_fact['client']['nom_client']).first()
    except Exception as e :
        print("error in client_existe :", e)
        client_existe = None


    if client_existe :
        print("client_existe :", client_existe)
    else:
        adresse_dict = dict_fact['client']['addesse_client']
        print("adresse_dict :", adresse_dict)
        if dict_fact['client']['addesse_client']['1'] == None and dict_fact['client']['addesse_client']['2'] == None :
            client = orm.Clients(
                nomClient = dict_fact['client']['nom_client'],
                adresse = f""
            )
        elif dict_fact['client']['addesse_client']['1'] == None :
            client = orm.Clients(
                nomClient = dict_fact['client']['nom_client'],
                adresse = f"{dict_fact['client']['addesse_client']['2']}"
            )
        elif dict_fact['client']['addesse_client']['2'] == None :
            client = orm.Clients(
                nomClient = dict_fact['client']['nom_client'],
                adresse = f"{dict_fact['client']['addesse_client']['1']}"
            )
        else :
            client = orm.Clients(
                nomClient = dict_fact['client']['nom_client'],
                adresse = f"{dict_fact['client']['addesse_client']['1']}, {dict_fact['client']['addesse_client']['2']}"
            )

        # Ajout du client à la session
        session.add(client)
        session.commit()

    # ========== traitement de la facture ==========

    # Vérification si la facture existe déjà dans la base de données
    try :
        facture_existe = session.query(orm.Factures).filter_by(idFacture=dict_fact['facture']['id_facture']).first()
    except Exception as e :
        print("error in facture_existe :", e)
        facture_existe = None

    if facture_existe :
        print("facture_existe :", facture_existe)
    else:
        if client_existe :
            id_client = client_existe.idClient
            print("id_client_existe :", id_client)
        else:
            id_client = client.idClient
            print("id_client :", id_client)
        
        facture = orm.Factures(
            idFacture = dict_fact['facture']['id_facture'],
            imagePath = dict_fact['facture']['image_facture'],
            idClient = id_client,
            total = dict_fact['facture']['total_facture'],
            dateFacture = dict_fact['facture']['date_facture']
        )
    
        # Ajout de la facture à la session
        session.add(facture)
        session.commit()

    # ========== traitement du produit et de l'achat ==========
    
    list_produits = dict_fact['produit']
    list_achats = dict_fact['achat']
    print("list_produits :", list_produits, "list_achats :", list_achats)

    for dict_element in list_produits :
        # Vérification si la facture existe déjà dans la base de données
        try :
            produit_existe = session.query(orm.Produits).filter_by(nomProduit=dict_element['nom_produit']).first()
        except Exception as e :
            print("error in produit_existe :", e)
            produit_existe = None
        
        if produit_existe :
            try :
                achat_existe = session.query(orm.Achats).filter_by(idProduit=produit_existe.idProduit).filter_by(idFacture=dict_fact['facture']['id_facture']).first()
            except Exception as e :
                print("error in achat_existe :", e)
                achat_existe = None
            
            if achat_existe :
                print("produit_existe :", produit_existe)
                print("achat_existe :", achat_existe)
            else:
                for dict_achat in list_achats :
                    if dict_achat['id_produit'] == dict_element['nom_produit'] :
                        achat = orm.Achats(
                            idProduit = produit_existe.idProduit,
                            idFacture = dict_fact['facture']['id_facture'],
                            quantites = dict_achat['quantite_produit']
                        )
                        # Ajout de l'achat à la session
                        session.add(achat)
                        session.commit()
                print("produit_existe :", produit_existe)
        else :
            produit = orm.Produits(
                nomProduit = dict_element['nom_produit'],
                prix = dict_element['prix_produit']
            )
            # Ajout du produit à la session
            session.add(produit)
            session.commit()

            try :
                achat_existe = session.query(orm.Achats).filter_by(idProduit=produit_existe.idProduit).filter_by(idFacture=dict_fact['facture']['id_facture']).first()
            except Exception as e :
                print("error in achat_existe :", e)
                achat_existe = None
            
            if achat_existe :
                print("achat_existe :", achat_existe)
            else:
                for dict_achat in list_achats :
                    if dict_achat['id_produit'] == dict_element['nom_produit'] :
                        achat = orm.Achats(
                            idProduit = produit.idProduit,
                            idFacture = dict_fact['facture']['id_facture'],
                            quantites = dict_achat['quantite_produit']
                        )
                        # Ajout de l'achat à la session
                        session.add(achat)
                        session.commit()
            
    # ========== traitement du monitoring ==========

    date_monitoring = datetime.datetime.today()
    monitoring = orm.Monitoring(
        ocrStatut = dict_fact['monitoring']['OCR_statut'],
        codeErrorOCR = dict_fact['monitoring']['code_error_OCR'],
        bdStatut = dict_fact['monitoring']['BD_statut'],
        codeErrorBD = dict_fact['monitoring']['code_error_BD'],
        idFacture = dict_fact['facture']['id_facture'],
        dateMonitoring = date_monitoring
    )

    # Ajout du monitoring à la session
    session.add(monitoring)
    session.commit()

# to_BD_result = {'facture': {'id_facture': 'FAC_2019_0005', 
#                             'image_facture': 'https://invoiceocrp3.azurewebsites.net/static/FAC_2019_0005-1869518.png', 
#                             'total_facture': '1661.00', 'date_facture': '2019-01-03'}, 
#                 'client': {'id_client': None, 'nom_client': 'Victoria Parker', 'addesse_client': {'1': 'USCGC Park', '2': None}}, 
#                 'produit': [{'id_produit': 'Caractère sein erreur faute', 'nom_produit': 'Caractère sein erreur faute', 'prix_produit': 31.32}], 
#                 'achat': [{'id_produit': 'Caractère sein erreur faute', 'quantite_produit': 6}], 
#                 'monitoring': {'id_monitoring': None, 'OCR_statut': None, 'code_error_OCR': None, 'BD_statut': None, 'code_error_BD': None}}

# dict_con = connect_bd()
# session = dict_con['session']
# get_dict_to_bd(to_BD_result, session)

# ========================================
# methode pour récupérer données pour statistique comptable
# ========================================
def get_df_stat (session, engine) :
    # df_facture
    df_query_facture = session.query(orm.Factures)
    df_facture = pd.read_sql( sql=df_query_facture.statement, con=engine )

    # df_client
    df_query_client = session.query(orm.Clients)
    df_client = pd.read_sql( sql=df_query_client.statement, con=engine )

    # df_produit
    df_query_produit = session.query(orm.Produits)
    df_produit = pd.read_sql( sql=df_query_produit.statement, con=engine )

    # df_facture
    df_query_achat = session.query(orm.Achats)
    df_achat = pd.read_sql( sql=df_query_achat.statement, con=engine )

    return {'df_facture':df_facture, 'df_client':df_client, 'df_produit':df_produit, 'df_achat':df_achat}

# ========================================
# méthode pour récupérer données pour statistique monitoring
# ========================================
def get_df_monitoring (session, engine) :
    df_query = session.query(orm.Monitoring).order_by(orm.Monitoring.dateMonitoring)
    
    df = pd.read_sql( sql=df_query.statement, con=engine )

    return df

# dict_con = connect_bd()
# session = dict_con['session']
# engine = dict_con['engine']

# df_monit = get_df_monitoring(session, engine)
# print('df_monit :', df_monit)