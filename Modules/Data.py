from Modules.Symbols import symbols as sb
from Modules.Save import save_to
from datetime import datetime

import yfinance as yf




def get_key(value):
    
    """
    get_key la fonction cherche dans le dictionnaire des symbols la cle qui correspond a la valeur passee en parametre

    Args:
        value (string): _description_ le symbol d'une action du cac40

    Returns:
        key_wanted _type_: _description_ la cle qui correspond a la value
    """
    
    key_wanted = None
    for key, values_in_dict in sb.items():
        if values_in_dict == value:
            key_wanted = key
            break

    if key_wanted is not None:
        return key_wanted

def temps_reel_data(symbols):
    
    """
    temps_reel_data la fonction calcul le cours d'une action ou plusieurs a temps reel et affiche le resultat sur la sortie standard

    Args:
        symbols (liste): _description_ prend une liste de symbols
    """
    for elem in symbols:
        
        print(f"\n{get_key(elem)}")
        data = yf.download(elem,start="2024-02-28")
        print(data)
        

def process_hist(symbol,data):
    
    print("\nVeuillez choisir une option:\n")
    print("1- Stocker l'historique dans un fichier\n2- Visualiser l'historique (Graphe)\n3- Retour\n")
    option = int(input())
    if option == 1:
        print("\nVeuillez choisir le format du fichier (csv/xls):\n")
        format  = input()
        save_to(get_key(symbol),data,format)
    
def history(symbol, start, end, interval, period,option):
    
    if option == 1:
        data = yf.download(symbol,start=start,end=end,interval=interval)
    elif option == 2:
        data = yf.download(symbol,period=period)
        
    process_hist(symbol,data)
    print(data)