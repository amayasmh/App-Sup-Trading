
from Modules.Symbols import symbols as sb
from Modules.Save import save_to
from Modules.Viz import viz
from datetime import datetime, timedelta

import yfinance as yf
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO, filename="./Log/SupTrading.log", filemode="a", format='%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)



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
    Télécharge et traite les données en temps réel pour une liste de symboles boursiers.

    :param symbols: Une liste de chaînes de caractères représentant les symboles boursiers à traiter.
    :return: Un DataFrame pandas contenant les dernières données pour tous les symboles fournis.
             Si aucune donnée n'est récupérée, retourne un DataFrame vide.
    """
    
    final_rows = []  # Liste pour stocker la dernière ligne de chaque symbole
    for elem in symbols:
        share = get_key(elem)  # Assurez-vous que la fonction get_key est définie correctement
        now = datetime.now()
        start = now - timedelta(minutes=120)
        data = yf.download(elem, start=start, interval="1m")
        #print(data)
        try:
            data.reset_index(inplace=True)
            data['share'] = share
            data['symbol'] = elem
            desired_columns = ['Datetime', 'share', 'symbol', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
            data = data[desired_columns]

            data.rename(columns={'Datetime': 'date', 'Adj Close': 'adj_close'}, inplace=True)
            data.columns = data.columns.str.lower()
            final_row = data.tail(1)  # Prendre la dernière ligne
            final_rows.append(final_row)
        except:
            print(f"\nL'action n'a pas été retrouvée : {share}\n")
    
    if final_rows:
        return pd.concat(final_rows)  # Retourner un DataFrame contenant les dernières lignes pour tous les symboles
    else:
        
        return pd.DataFrame()  # Retourner un DataFrame vide si aucune donnée n'est récupérée
 

def process_hist(symbol,data):
    
    """
    Traite l'historique d'un symbole en proposant à l'utilisateur de stocker les données dans un fichier,
    de visualiser l'historique via un graphique, ou de retourner au menu précédent.

    :param symbol: Symbole boursier dont l'historique est traité.
    :param data: DataFrame contenant l'historique du symbole.
    :return: Le code d'option choisi par l'utilisateur.
    """
    
    logger.info(f"Traitement de l'historique pour le symbole {symbol}.")
    print("\nVeuillez choisir une option:\n")
    print("1- Stocker l'historique dans un fichier\n2- Visualiser l'historique (Graphe)\n3- Retour\n")
    option = int(input())
    
    if option == 1:
        logger.info(f"Option 1 choisie pour le symbole {symbol}.")
        while(1):
            
            print("\nVeuillez choisir le format du fichier (csv/xlsx):\n")
            format  = input()
            if save_to(get_key(symbol),data,format):
                break 
    
    elif option == 2:
        logger.info(f"Option 2 choisie pour le symbole {symbol}. Visualisation de l'historique.")
        viz(data)
    
    elif option == 3:
        return 3
    
    else:
        print("Oupssss, option non disponible")
        return 4
    
    return option
    
def history(symbol, start, end, interval, period, option):
    
    """
    Télécharge et traite l'historique boursier d'un symbole donné pour une période spécifiée.

    :param symbol: Symbole boursier à analyser.
    :param start: Date de début pour le téléchargement des données (utilisé avec option 1).
    :param end: Date de fin pour le téléchargement des données (utilisé avec option 1).
    :param interval: Intervalle des données à télécharger.
    :param period: Période de téléchargement des données (utilisé avec option 2).
    :param option: Option de téléchargement (1 pour un intervalle spécifique, 2 pour une période).
    :return: None
    """ 
    
    if option == 1:
        logger.info(f"Téléchargement des données pour {symbol} du {start} au {end} avec un intervalle de {interval}.")
        data = yf.download(symbol, start=start, end=end, interval=interval)
    elif option == 2:
        logger.info(f"Téléchargement des données pour {symbol} sur la période {period}.")
        data = yf.download(symbol, period=period)
    
    data.reset_index(inplace=True)
    
    
    share = get_key(symbol)
    data['share'] = share
    data['symbol'] = symbol
    
    desired_columns = ['Date', 'share', 'symbol', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    
    # Assurez-vous que toutes les colonnes dans `desired_columns` existent dans `data` avant de filtrer
    data = data[[col for col in desired_columns if col in data.columns]]
    
    #data.rename(columns={'Datetime': 'date'}, inplace=True)
    data.rename(columns={'Adj Close': 'adj_close'}, inplace=True)
    data.columns = data.columns.str.lower()   
    print(data)    
    while(process_hist(symbol, data) != 3):
        continue
    
    logger.info(f"Fin du traitement pour {symbol}.")