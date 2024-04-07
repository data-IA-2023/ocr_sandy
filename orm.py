"""
=========================================
classe :
    orm
methode :
    connectBd 
    createsession
=========================================
classe :
    Factures
attribus :
    idFacture
    imagePath
    idClient
    total
    dateFacture
=========================================
classe :
    Clients
attribus :
    idClient
    nomClient 
    adresse
=========================================
classe :
    Produits
attribus :
    idProduit
    nomProduit
    prix
=========================================
classe :
    Achats
attribus :
    idAchat
    idFacture
    idProduit
    quantites
=========================================
classe :
    Monitoring
attribus :
    idMonitoring
    ocrStatut
    codeErrorOCR
    bdStatut
    codeErrorBD
    idFacture
    dateMonitoring
=========================================
"""

# =========================================
# importation :
# =========================================
from sqlalchemy import ForeignKey, create_engine, Column, String, DateTime, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from dotenv import load_dotenv
import os
import pyodbc

# =======================    connection à la base de données    =======================

def connectBd():
    try:
        # Trouve le chemein du fichier .env et l'ouvre par dotenv
        repertoir_fichier = os.path.dirname(__file__)
        env_path = f'{repertoir_fichier}/.env'
        load_dotenv(dotenv_path=env_path)

        SERVER = os.environ.get('SERVER')
        DATABASE = os.environ.get('DATABASE')
        USERNAME = os.environ.get('USERNAME')
        PASSWORD = os.environ.get('PASSWORD')
        
        connectionString = f'mssql+pyodbc://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver=ODBC+Driver+18+for+SQL+Server'

        engine = create_engine(connectionString) 
        
        Base.metadata.create_all(engine)
    
    except Exception as e:
        print(f"Erreur lors de la connexion à la BD OCR: {e}")
        return None
    else:
        return engine

def createsession(engine):
    # Création de la session en utilisant l'engine passé en paramètre
    Session = sessionmaker(bind=engine, autoflush=False)
    session = Session()
    session.autocommit = True
    return session
# =======================    classe des classe de la base de données    =======================

# déclaraction de la classe de basse de sqlalchimy
# tous les modèles en hérite
Base = declarative_base()

# clase pour la table Factures
class Factures ( Base ):
    __tablename__ = "factures"
    __table_args__ = {'schema': 'dbo'}

    idFacture = Column(String(25), primary_key=True)
    imagePath = Column(String(100))
    idClient = Column(Integer, ForeignKey('dbo.clients.idClient'))  # Spécification du schéma
    total = Column(Integer)
    dateFacture = Column(DateTime)

    # Définir la relation avec la table "clients"
    client = relationship("Clients", back_populates="facture")
    # Définir la relation avec la table "Achats"
    achat = relationship("Achats", back_populates="facture")
    # Définir la relation avec la table "Monitoring"
    monitoring = relationship("Monitoring", back_populates="facture")

# clase pour la table Clients
class Clients ( Base ):
    __tablename__ = "clients"
    __table_args__ = {'schema': 'dbo'}

    idClient = Column(Integer, primary_key=True, autoincrement=True)
    nomClient = Column(String(100))
    adresse = Column(String(500))

    # Définir la relation avec la table "Factures"
    facture = relationship("Factures", back_populates="client")

# clase pour la table Produits
class Produits ( Base ):
    __tablename__ = "produits"
    __table_args__ = {'schema': 'dbo'}

    idProduit = Column(Integer, primary_key=True, autoincrement=True)
    nomProduit = Column(String(100))
    prix = Column(Integer)

    # Définir la relation avec la table "Achats"
    achat = relationship("Achats", back_populates="produit")

# clase pour la table Achats
class Achats ( Base ):
    __tablename__ = "achats"
    __table_args__ = {'schema': 'dbo'}

    idAchat = Column(Integer, primary_key=True, autoincrement=True)
    idFacture = Column(String(25), ForeignKey('dbo.factures.idFacture'))
    idProduit = Column(Integer, ForeignKey('dbo.produits.idProduit'))
    quantites = Column(Integer)
    
    # Définir la relation avec la table "Produits"
    produit = relationship("Produits", back_populates="achat")
    # Définir la relation avec la table "Factures"
    facture = relationship("Factures", back_populates="achat")

# clase pour la table Monitoring
class Monitoring ( Base ):
    __tablename__ = "monitoring"
    __table_args__ = {'schema': 'dbo'}

    idMonitoring = Column(Integer, primary_key=True, autoincrement=True)
    ocrStatut = Column(String(50))
    codeErrorOCR = Column(String(500))
    bdStatut = Column(String(50))
    codeErrorBD = Column(String(500))
    idFacture = Column(String(25), ForeignKey('dbo.factures.idFacture'))
    dateMonitoring = Column(DateTime)
    
    # Définir la relation avec la table "Factures"
    facture = relationship("Factures", back_populates="monitoring")

# =======================    méthode de la base de données    =======================

con = connectBd()

print(con)

sess = createsession(con)

print(sess)