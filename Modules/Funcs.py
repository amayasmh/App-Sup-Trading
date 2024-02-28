from Modules.Symbols import symbols
from Modules.Data import temps_reel_data
from datetime import datetime

import logging



logging.basicConfig(level=logging.INFO, filename="./Log/SupTrading.log", filemode="a", format='%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


def menu():
    
    """
    la fonction affiche un menu d'options qui permettra a l'utilisateur de suivre a temps reel ou de d'afficher l'historique des actions ainsi que de quitter l'appli

    Returns:
        option : entier (int)
        
    """
    
    logger.info("Affichage du menu principal")
    
    print("\nMenu Principal\nVeuillez choisir une option:\n")
    print("1- Suivre le cours des actions a temps reel\n2- Afficher l'historique des actions\n3- Afficher les symboles des actions\n4- Quitter")
    
    try:
        option = int(input("\n"))
      
    except ValueError:
        print("Oupssss, l'option n'est pas valide !")
        menu()
        
    return option


def tr_process_option(option):
    
    if option == 1:
        symbol = input("\nVeuillez saisir le symbole de l'action:\n\n")
        if symbol not in symbols.values():
            print("\nOupssss, aucune action ne correspond a ce symbole")
            return True
            
        else:
            temps_reel_data([symbol])
    
    elif option == 2 :
        temps_reel_data(symbols.values())
            
    
def temps_reel_menu():
    
    print("\nVeuillez choisir une option:\n")
    print("1- Saisir le symbole d'une action\n2- Toutes les actions\n3- Retour")
    
    try:
        opt = int(input("\n"))
        
    except ValueError:
        print("Oupssss, l'option n'est pas valide !")
        temps_reel_menu()
        
    return opt

def process_options(option):
    
    if option == 1 :
        
        logger.info("Suivi a temps reel")
        
        heure_actuelle = datetime.now().time()
        heure = heure_actuelle.hour
        minute = heure_actuelle.minute
        print("\nHeure actuelle:", heure, ":", minute)
        
        if heure < 9 and (heure >= 17 and minute > 30):
            print("Le marché est fermé") 
            
        else:
            
            while(1):
                
                trOption = temps_reel_menu()
                if trOption == 3:
                    break
                if not tr_process_option(trOption):
                    break
                    
        return True
    
    elif option == 2:
        print
        return True
    elif option == 3:
    
        logger.info("Affichage des symboles des actions")
        print(symbols)
        return True
        
    else:
        print("Option non disponible")
        return True