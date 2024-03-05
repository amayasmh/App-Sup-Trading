
import openpyxl
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, filename="./Log/SupTrading.log", filemode="a", format='%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


def save_to(action,data, ext):
    heure_actuelle = datetime.now()
 
    if ext == "csv":
        
        try:
            data.to_csv(f"./Files/{action}_historique_{heure_actuelle}.csv",index=False)
            print("\nFichier sauvegardé\n")
            return True
        except:
            print("\nOupssss, un probleme est survenu\n")
            return False
        
    elif ext == "xlsx":
        
        try:
            
            data.to_excel(f"./Files/{action}_historique_{heure_actuelle}.xlsx", index=False)
            print("\nFichier sauvegardé\n")
            return True
        except Exception as e:
            print(f"\nOupssss, un problème est survenu: {e}\n")
            return False

    else:
        print("\nOupssss, extention incorrecte\n")
        return False
    