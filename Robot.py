import json
from Modules.DataBaseFuncs import connect, create_table, create_trigger, insert_data
from Modules.Data import temps_reel_data
from Modules.Symbols import symbols
from Modules.SendMail import SendMail
from datetime import datetime
import pandas as pd
import time  # Importer le module time

cursor, connexion = connect()
create_table("cac40_daily_data", cursor, connexion)
create_table("cac40_history_data", cursor, connexion)
create_trigger(cursor, connexion)

def should_run(hour, minute):
    return 9 <= hour < 17 or (hour == 17 and minute <= 30)

last_data = pd.DataFrame(columns=['date', 'share', 'symbol', 'open', 'high', 'low', 'close', 'adj_close', 'volume'])

# Ouvrir un fichier pour stocker les temps d'exécution
execution_time_file = 'execution_times.txt'

while True:
    current_time = datetime.now()
    hour = current_time.hour
    minute = current_time.minute
    
    if not should_run(hour, minute):
        print("\nHors des heures de trading. Heure actuelle: ", hour, ":", minute)
        break  # Sortie de la boucle si hors des heures de trading
    
    # Mesurer le temps de récupération des données
    data_start_time = time.time()
    returned_data = temps_reel_data(symbols.values())  # Récupérer les données
    data_end_time = time.time()
    data_retrieval_time = data_end_time - data_start_time
    print(returned_data)

    if not returned_data.empty:
        insertion_all_time = 0  # Initialiser le temps total d'insertion           
        for index, row in returned_data.iterrows():
            if not ((last_data['date'] == row['date']) & (last_data['symbol'] == row['symbol'])).any():
                print("\nNouvelle donnée détectée. Heure actuelle:", hour, ":", minute)
                
                # Mesurer le temps d'insertion des données
                insert_start_time = time.time()
                insert_data("cac40_daily_data", cursor, connexion, dict(row))  
                insert_end_time = time.time()
                insertion_time = insert_end_time - insert_start_time
                insertion_all_time += insertion_time
                
            else:
                print("\nDonnée existante. Heure actuelle:", hour, ":", minute)
        
        last_data = returned_data.copy()  
        
        with open(execution_time_file, 'a') as file:
            file.write(f'Temps de récupération des données: {data_retrieval_time} secondes\n')
            if insertion_all_time > 0:  # Écrire le temps d'insertion seulement s'il y a eu des insertions
                file.write(f"Temps total d'insertion: {insertion_all_time} secondes\n")
    else:
        print("\nAucune nouvelle donnée. Heure actuelle:", hour, ":", minute)
    
    
    # Vider la table si l'heure est 17h55
    if hour == 11 and minute >= 36:
        
        # Récupérer toutes les données de la table
        cursor.execute("SELECT * FROM cac40_daily_data")
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=['index','date', 'share', 'symbol', 'open', 'high', 'low', 'close', 'adj_close', 'volume'])
        
        # Exporter les données dans un fichier CSV
        csv_file_name = f'Files/cac40_daily_data_backup_{datetime.now()}.csv'
        df.to_csv(csv_file_name, index=False)
        print(f"Les données ont été exportées dans le fichier {csv_file_name}.")
        
        #envoi de mail
        SendMail(f"Copie des donnees du cac40 {datetime.now()}","Bonjour\n Voici le fichier du cours des actions du CAC40 pour aujourd'hui\n Cordialement Equipe IT",csv_file_name)
        
        cursor.execute("TRUNCATE TABLE cac40_daily_data")
        connexion.commit()
        print("Table cac40_daily_data vidée.")  
        break
        
          
cursor.close()
connexion.close()
