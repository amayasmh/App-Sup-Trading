from Modules.Symbols import symbols
from Modules.Data import temps_reel_data, history
from datetime import datetime

import logging
import re


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
        print("\nOupssss, saisie invalide !")
        menu()
        
    return option


def tr_process_option(option):
    
    """
    tr_process_option la fonction traite l'option choisi par l'utilisateur dans la partie suivi a temps reel

    Args:
        option (int): _description_ l'option choisi par l'utilisateur

    Returns:
        True/False (bool): _description_ renvoie True pour reafficher le menu et False pour sortir
    """
    
    if option == 1: #Suivi d'une seule action
        logger.info("Suivre a temps reel une seule action")
        print("\n")
        print(symbols)
        print("\n")
        symbol = input("\nVeuillez saisir le symbole de l'action:\n\n")
        if symbol not in symbols.values():
            print("\nOupssss, aucune action ne correspond a ce symbole")
            return True
            
        else:
            print(temps_reel_data([symbol]))
    
    elif option == 2 : #Suivi de toutes les actions
        logger.info("Suivre a temps reel toutes les actions du CAC40")
        print(temps_reel_data(symbols.values()))
    
    else: #Cas d'une saise incorrecte (le menu secondaire sera afficher a nouveau)
        print("\nOupssss,option non disponible")
        return True
            
    
def tr_menu():
    
    """
    tr_menu le sous menu qui affiche les options suire une seule action ou toutes et aussi une option retour pour revenir vers le premier menu

    Returns:
        opt (int): _description_ l'option choisi par l'utilisateur
    """
    
    logger.info("Affichage du menu de l'option temps reel")
    

    print("\nVeuillez choisir une option:\n")
    print("1- Saisir le symbole d'une action\n2- Toutes les actions\n3- Retour")
    
    try:
        opt = int(input("\n"))
        
    except ValueError:
        print("Oupssss, saisie invalide !")
        tr_menu()
        
    return opt


def hist_process_option(symbol,option):
    
    if option == 1:
        
        pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        start = input("\nVeuillez saisir la date de début (Format : AAAA-MM-JJ):\n")
        
        if not pattern.match(start):
            print("\nOupssss, le format de la date n'est pas correcte\n")
            return True
        
        end = input("\nVeuillez saisir la date de fin (Format : AAAA-MM-JJ) ou None:\n")
        
        if not pattern.match(end):
            if end == "None":
                
                end = None
            else:
                print("\nOupssss, le format de la date n'est pas correcte\n")
                return True
                
        
        print("\nVeuillez saisir l'interval souhaiter (1m/5m/1h/1d/5d/1wk/1mo/3mo):\n")        
        interval = input("\n")
        
        if interval not in ["1m","5m","1h","1d","5d","1wk","1mo","3mo"]:
            print("\nOupssss, l'interval choisi n'est pas correcte\n")
            return True
        
        history(symbol,start,end,interval,period=None,option=1)
        
    elif option == 2:
        
        print("\nVeuillez saisir une période (1d/5d/1mo/3mo/6mo/1y/2y):\n") 
        period = input("")
        
        if period not in ["1d","5d","1mo","3mo","6mo","1y","2y"]:
            print("\nOupssss, la period choisie n'est pas correcte\n")
            return True
        
        history(symbol,start=None,end=None,interval=None, period=period,option=2)
    
    else: #Cas d'une saise incorrecte (le menu secondaire sera afficher a nouveau)
        
        print("\nOupssss,option non disponible")
        return True
    
def hist_menu():
    
    print("\n")
    print(symbols)
    
    try:
        
        symbol = input("\nVeuillez saisir le symbol de l'action:\n\n")
        
        if symbol not in symbols.values():
            print("\nOupssss, Aucune action ne correspond a ce symbol")
            return symbol,4
        
        print("\nVeuillez choisir une option:\n")
        option = int(input("1- Par date (Début/Fin) + Intervale\n2- Par période\n3- Retour\n\n"))
        
        
    except ValueError:
        
        print("Oupssss, saisie invalide !")
        hist_menu()
        
    return symbol,option
    
    
def process_options(option):
    
    """process_options la fonction traite l'option saisie par l'utilisateur dans le menu principal

    Args:
        option (int): _description_ option saisie

    Returns:
        True/False (bool): _description_ false pour arreter la boucle principal ou true pour reafficher le menu
    """
    if option == 1 : #Cas de suivi a temps reel
        
        logger.info("Suivi a temps reel")
        
        current_time = datetime.now().time()
        hour = current_time.hour
        minute = current_time.minute
        print("\nHeure actuelle:", hour, ":", minute)
        
        if hour < 9 or hour >= 18 or (hour == 17 and minute >= 30):
            print("Le marché est fermé") 

        else:
            
            while(1): # Boucle infinie pour afficher le sous menu pour le suivi a temps reel
                
                
                trOption = tr_menu()
                if trOption == 3:
                    logger.info("Retour vers le menu principal")
                    break
                if not tr_process_option(trOption):
                    break
                    
        return True
    
    elif option == 2: #Cas d'affichage d'historique
        logger.info("Données historique")
        
        while(1):
            
            symbol,opt = hist_menu()
            
            if opt == 3:
                
                logger.info("Retour vers le menu principal")
                break
            if opt == 4:
                continue
            elif not hist_process_option(symbol,opt):
                break
            
        return True
    
    elif option == 3: #Affichage des symbols
        
        logger.info("Affichage des symboles des actions")
        print(symbols)
        return True
        
    else: #Cas de saisie incorrecte
        logger.info("Saisie incorrecte")
        print("\nOupssss,option non disponible")
        return True