from datetime import datetime
import logging

# Configuration du logger
logging.basicConfig(level=logging.INFO, filename="./Log/SupTrading.log", filemode="a", format='%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def save_to(action, data, ext):
    """
    Sauvegarde les données dans un fichier CSV ou Excel en fonction de l'extension spécifiée.

    :param action: Nom de l'action ou identifiant pour nommer le fichier.
    :param data: DataFrame contenant les données à sauvegarder.
    :param ext: Extension du fichier pour déterminer le format de sauvegarde ('csv' ou 'xlsx').
    """
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    if ext == "csv":
        filename = f"./Files/{action}_historique_{current_time}.csv"
        try:
            data.to_csv(filename, index=False)
            logger.info(f"Fichier {filename} sauvegardé avec succès.")
            print("\nFichier sauvegardé\n")
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde du fichier {filename}: {e}", exc_info=True)
            print("\nOupssss, un problème est survenu\n")
            return False
        
    elif ext == "xlsx":
        filename = f"./Files/{action}_historique_{current_time}.xlsx"
        try:
            data.to_excel(filename, index=False)
            logger.info(f"Fichier {filename} sauvegardé avec succès.")
            print("\nFichier sauvegardé\n")
            return True
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde du fichier {filename}: {e}", exc_info=True)
            print(f"\nOupssss, un problème est survenu: {e}\n")
            return False
    else:
        logger.warning(f"Extension '{ext}' incorrecte. Aucun fichier n'a été sauvegardé.")
        print("\nOupssss, extension incorrecte\n")
        return False
