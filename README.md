# ocr_sandy

## Contexte du projet

En tant que développeur⸱se en IA pour le compte d’une ESN, vous devez :

    - Intégrer la connexion à l’API Azure Cognitives Services
    - Intégrer les appels aux fonctions d’OCR
    - Extraire les informations pertinentes
    - Calculer les métriques attendues à partir des résultats de l’API
    - Identifier un seuil de qualité minimum pour l'OCR
    - Stocker les résultats en base de données
    - Automatiser le processus complet, depuis la facture jusqu'au stockage en base de données
    - Intégrer les résultats dans une interface web simple
    - Documenter, versionner, livrer

## Livrables

  - Une base de données alimentées
  - Dépôt Github : avec .gitignore, requirements.txt, readme, et tous les autres scripts
  - Un rapport écrit de 5 pages mini : présentation du projet, présentation de l'OCR (principe, méthode et fonctionnement, limites, etc.)
  - Trello du projet

  - Une appli web fonctionnelle avec :
    - Une page pour l'OCR d'une facture (démo)
    - Une page pour le reporting automatisé de la comptabilité fournisseurs
    - Une page pour le monitoring du service Azure OCR

  - Slides de présentation du projet avec au moins les éléments suivants :
    - Schéma fonctionnel de l’application avec les services nécessaires les technologies utilisées
    - Identification des services d'IA existants et utilisés. Savoir expliquer leur fonctionnement
    - Liste des spécifications fonctionnelles de l’application

## Critères de performance

L'application finale doit :
  - Correspondre aux objectifs énoncés
  - Intégrer tous les services nécessaires à son bon fonctionnement

Bonus :
  - La procédure en cas de résultat en deçà d’un seuil de qualité minimum est appliquée
  - L'application peut intégrer les modalités du "ML Feedback loop".
  - L'application peut intégrer un template "user friendly"
  - L'application est sécurisée selon le top 10 OWASP
  - L'application est Dockerisée
  - L'application offre le choix d'utiliser soit le service OCR par Azure (payant) ou le service OCR Python (développement ad'hoc, gratuit)
