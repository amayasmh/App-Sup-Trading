

from datetime import datetime


def save_to(action,data, ext):
    heure_actuelle = datetime.now()
    data_copy = data.copy()
    data_copy.insert(0,"action",action)
    if ext == "csv":
        data_copy.to_csv(f"./Files/{action}_historique_{heure_actuelle}.csv",index=False)
    print(data_copy)