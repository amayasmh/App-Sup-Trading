
import os
import traceback
from Modules.DataBaseFuncs import connect, create_table, create_trigger, insert_data
from Modules.Data import temps_reel_data
from Modules.Symbols import symbols
from Modules.SendMail import send_mail
from datetime import datetime
import pandas as pd
import time  # Importer le module time



def should_run(hour):
    return 9 <= hour < 18 


current_time = datetime.now()
hour = current_time.hour
minute = current_time.minute

if should_run(hour):
    
    try:
        
    
        print("debut")
        cursor, connexion = connect()
        create_table("cac40_daily_data", cursor, connexion)
        create_table("cac40_history_data", cursor, connexion)
        create_trigger(cursor, connexion)
        last_data = pd.DataFrame(columns=['date', 'share', 'symbol', 'open', 'high', 'low', 'close', 'adj_close', 'volume'])

        # Le fichier pour stocker les temps d'exécution
        execution_time_file = 'execution_times.txt'

        while True:
            current_time = datetime.now()
            hour = current_time.hour
            minute = current_time.minute
            
            if not should_run(hour):
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
                        print("\nNouvelle donnée détectée.")
                        
                        # Mesurer le temps d'insertion des données
                        insert_start_time = time.time()
                        insert_data("cac40_daily_data", cursor, connexion, dict(row))  
                        insert_end_time = time.time()
                        insertion_time = insert_end_time - insert_start_time
                        insertion_all_time += insertion_time
                        
                    else:
                        print("\nDonnée existante.")
                
                last_data = returned_data.copy()  
                
                with open(execution_time_file, 'a') as file:
                    file.write(f'Temps de récupération des données: {data_retrieval_time} secondes\n')
                    if insertion_all_time > 0:  # Écrire le temps d'insertion seulement s'il y a eu des insertions
                        file.write(f"Temps total d'insertion: {insertion_all_time} secondes\n")
            else:
                print("\nAucune nouvelle donnée. Heure actuelle:", hour, ":", minute)
            
            
            # Vider la table si l'heure est 17h59
            if hour == 17 and minute >= 59:
                
                # Récupérer toutes les données de la table
                cursor.execute("SELECT * FROM cac40_daily_data")
                rows = cursor.fetchall()
                df = pd.DataFrame(rows, columns=['index','date', 'share', 'symbol', 'open', 'high', 'low', 'close', 'adj_close', 'volume'])
                
                # Exporter les données dans un fichier CSV
                csv_file_name = f'Files/cac40_daily_data_{datetime.now()}.csv'
                df.to_csv(csv_file_name, index=False)
                print(f"Les données ont été exportées dans le fichier {csv_file_name}.")
                
                #envoi de mail
                send_mail(f"Copie des donnees du cac40 {datetime.now()}","Bonjour\nVoici le fichier du cours des actions du CAC40 pour aujourd'hui\nCordialement Equipe IT",csv_file_name)
                
                cursor.execute("TRUNCATE TABLE cac40_daily_data RESTART IDENTITY")
                connexion.commit()
                print("Table cac40_daily_data vidée.")  
                break
                
                
        cursor.close()
        connexion.close()
    

    except Exception as e:
        print("Oupssss, un probleme est survenu")
        # Obtenir la date et l'heure actuelle
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Formater le message d'erreur
        error_message = f"Erreur survenue le {current_time}\n\n"
        error_message += "Détails de l'erreur :\n"
        error_message += str(e) + "\n\n"
        error_message += "Traceback:\n"
        error_message += traceback.format_exc()
        
        # Nom du fichier de journalisation d'erreur avec timestamp
        error_log_file = f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Écriture de l'erreur dans le fichier
        with open(error_log_file, "w") as file:
            file.write(error_message)
        
        # Envoi de l'email avec le fichier d'erreur en pièce jointe
        send_mail("Erreur dans l'exécution du script Robot App-Sup-Trading", 
                "Une erreur s'est produite lors de l'exécution du script. Veuillez trouver les détails de l'erreur ci-joint.\n\n", 
                error_log_file)  # Assurez-vous que send_mail accepte une pièce jointe comme paramètre et est configurée pour traiter les pièces jointes correctement.
        
        print("Une alerte a été envoyée!")
        print("Fin du programme avec échec\n\n")
        
        os.remove(error_log_file)
        
    finally:
        # Assurez-vous de fermer les ressources dans un bloc finally
        if cursor is not None:
            cursor.close()
        if connexion is not None:
            connexion.close()
            
else:
    print("\nHors des heures de trading. Heure actuelle: ", hour, ":", minute)