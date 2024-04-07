"""
=========================================
classe :
    ocr
methode :
    OCR_image_to_dict => entée : lien d'une image, sortie : 2 dictionnaires
=========================================
"""

# =========================================
# importation :
# =========================================
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from dotenv import load_dotenv
import os

# =========================================
# classe et méthode :
# =========================================

# Trouve le chemein du fichier .env et l'ouvre par dotenv
repertoir_fichier = os.path.dirname(__file__)
# print(repertoir_fichier)
env_path = f'{repertoir_fichier}\\.env'
facture_path = f'{repertoir_fichier}\\statics\\factures\\FAC_2019_0998-5758105.png'
load_dotenv(dotenv_path=env_path)

try:
    endpoint = os.environ["OCR_ENDPOINT"]
    key = os.environ["OCR_KEY"]
except KeyError:
    print("Missing environment variable 'OCR_ENDPOINT' or 'OCR_KEY'")
    print("Set them before running this sample.")
    exit()

# Create an Image Analysis client
client = ImageAnalysisClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(key)
)

dict_bd = { 'facture' : {'id_facture': None, 'image_facture': None, 'total_facture': None, 
                         'date_facture': None},
           'client': {'id_client': None, 'nom_client': None, 'addesse_client': {"1":None, "2":None}},
           'produit': [],
           'achat': [],
           'monitoring': {'id_monitoring': None, 'OCR_statut': None, 'code_error_OCR': None,
                          'dict_statut': None, 'code_error_dict': None, 'BD_statut': None, 'code_error_BD': None}
            }

# ==============================================================

def OCR_image_to_dict (image_path="https://invoiceocrp3.azurewebsites.net/static/FAC_2019_0998-5758105.png", dict_result = dict_bd) :
    """
    entrée : le lien d'une image
    sortie : 2 dictionnaires ocr_dict et dict_result
    =====================================================================
    >>> OCR_image_to_dict("https://invoiceocrp3.azurewebsites.net/static/FAC_2019_0998-5758105.png")
    ocr_dict : [ 
        {'text_line': 'INVOICE FAC_2019_0998', 'Confidence': 0.962, 'polygon': [{'x': 17, 'y': 18}, {'x': 303, 'y': 17}, {'x': 303, 'y': 43}, {'x': 17, 'y': 44}]},
        {'text_line': 'Issue date 2019-12-18 18:21:00', 'Confidence': 0.9807, 'polygon': [{'x': 17, 'y': 49}, {'x': 308, 'y': 49}, {'x': 309, 'y': 70}, {'x': 17, 'y': 71}]}, 
        {'text_line': 'Bill to Ivan Abate', 'Confidence': 0.98, 'polygon': [{'x': 18, 'y': 79}, {'x': 166, 'y': 79}, {'x': 166, 'y': 99}, {'x': 18, 'y': 99}]}, 
        {'text_line': 'Brilllling', 'Confidence': 0.564, 'polygon': [{'x': 739, 'y': 94}, {'x': 809, 'y': 77}, {'x': 814, 'y': 92}, {'x': 744, 'y': 112}]}, 
        {'text_line': 'Address Canale Adele, 2 Piano 8', 'Confidence': 0.9893, 'polygon': [{'x': 17, 'y': 118}, {'x': 190, 'y': 118}, {'x': 190, 'y': 132}, {'x': 17, 'y': 132}]}, 
        {'text_line': '12053, Santuario Tinella (CN)', 'Confidence': 0.9918, 'polygon': [{'x': 19, 'y': 132}, {'x': 177, 'y': 133}, {'x': 177, 'y': 146}, {'x': 19, 'y': 145}]}, 
        {'text_line': 'TOTAL', 'Confidence': 0.997, 'polygon': [{'x': 38, 'y': 229}, {'x': 104, 'y': 229}, {'x': 104, 'y': 249}, {'x': 38, 'y': 249}]}, 
        {'text_line': '154.82 Euro', 'Confidence': 0.9925, 'polygon': [{'x': 548, 'y': 230}, {'x': 679, 'y': 231}, {'x': 679, 'y': 249}, {'x': 548, 'y': 248}]}, 
        {'text_line': 'Eos reprehenderit cumque culpa. 2 × 77.41 Euro', 'Confidence': 0.9415, 'polygon': [[{'x': 38, 'y': 200}, {'x': 321, 'y': 200}, {'x': 321, 'y': 220}, {'x': 38, 'y': 220}], [{'x': 511, 'y': 200}, {'x': 691, 'y': 201}, {'x': 691, 'y': 219}, {'x': 511, 'y': 218}]]}
    ]
    """
    try :
        # enregistre valeur dans dict_bd
        dict_result['facture']['image_facture']=image_path

        # print('image_path :', image_path)

        # Get a caption for the image. This will be a synchronously (blocking) call.
        result = client.analyze_from_url(
            image_url=image_path,
            visual_features=[VisualFeatures.CAPTION, VisualFeatures.READ],
            gender_neutral_caption=True,  # Optional (default is False)
        )

        # print("Image analysis results:")
        # Print caption results to the console
        # print(" Caption:")
        # if result.caption is not None:
        #     print(f"   '{result.caption.text}', Confidence {result.caption.confidence:.4f}")

        ocr_dict = []

        # Print text (OCR) analysis results to the console
        # print(" Read:")
        if result.read is not None:
            for line in result.read.blocks[0].lines:
                confidence_somme = 0
                confidence_nb = 0
                # print(f"   Line: '{line.text}', Bounding box {line.bounding_polygon}")
                for word in line.words:
                    # print(f"     Word: '{word.text}', Bounding polygon {word.bounding_polygon}, Confidence {word.confidence:.4f}")
                    confidence_somme = confidence_somme + word.confidence
                    confidence_nb += 1
                confidence_moyenne = round(confidence_somme/confidence_nb, 4)
                ocr_dict.append({"text_line": line.text, "Confidence": confidence_moyenne, "polygon": line.bounding_polygon})

        # print("ocr_dict :", ocr_dict)

        # règle le problème de ligne produit éclaté :
        element_ligne = False
        while element_ligne == False :
            count = 0
            # print("ici ", count)
            for element1, element2  in zip(ocr_dict[:-1], ocr_dict[1:]) :
                count += 1
                modifier = False
                y_pos_1 = element1['polygon'][0]['y']
                y_pos_2 = element2['polygon'][0]['y']
                # print(element1)
                # print(y_pos_1)
                # print(element2)
                # print(y_pos_2)
                if y_pos_1 == y_pos_2 or y_pos_1 == y_pos_2+1 or y_pos_1 == y_pos_2-1 or y_pos_1 == y_pos_2+2 or y_pos_1 == y_pos_2-2 :
                    element_text = element1['text_line']+' '+element2['text_line']
                    element_confience = (element1['Confidence']+element2['Confidence'])/2
                    ocr_dict[count-1] = {"text_line": element_text, "Confidence": element_confience, 
                                    "polygon": element1['polygon'] }
                    ocr_dict.remove(element2)
                    # print("ocr_dict modifief :", ocr_dict[count-1])
                    modifier = True
                    break
            if modifier == False :
                element_ligne = True
            # print("sortie ", element_ligne)

        dict_result['monitoring']['OCR_statut']= f'success'
        # print("ocr_dict :", ocr_dict)
        return ocr_dict, dict_result

    except HttpResponseError as e :
        dict_result['monitoring']['OCR_statut']= f'error in OCR_image_to_dict(), code :{e.status_code}, Reason: {e.reason}'
        dict_result['monitoring']['code_error_OCR']= e.error.message
        ocr_dict = False
        return ocr_dict, dict_result

# ==============================================================
