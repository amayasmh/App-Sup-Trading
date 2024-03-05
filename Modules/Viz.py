import logging
import matplotlib.pyplot as plt


logging.basicConfig(level=logging.INFO, filename="./Log/SupTrading.log", filemode="a", format='%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


def viz(data):
    # Extraire les dates, les valeurs d'ouverture (Open) et de clôture (Close) du DataFrame
    dates = data["date"]
    open_prices = data['open']
    close_prices = data['close']
    volume = data["volume"]
    
    # Créer le graphe
    fig, ax1 = plt.subplots(figsize=(10, 6))

    # Tracer les prix d'ouverture en vert
    color_open = 'green'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Prix', color=color_open)
    ax1.plot(dates, open_prices, marker='o', linestyle='-', color=color_open, label='Open')
    ax1.tick_params(axis='y', labelcolor=color_open)
    
    # Tracer les prix de clôture en rouge
    color_close = 'red'
    ax1.plot(dates, close_prices, marker='o', linestyle='-', color=color_close, label='Close')
    ax1.legend(loc='upper left')
    
    ax1.set_xticklabels(dates, rotation=45, ha="right")
    
    # Configuration de l'axe secondaire pour le volume
    ax2 = ax1.twinx()  # Instancier un second axe des ordonnées
    color_volume = 'tab:blue'
    ax2.set_ylabel('Volume', color=color_volume)  # Nous avons déjà géré l'étiquette x avec ax1
    ax2.plot(dates, volume, marker='o', linestyle='-', color=color_volume, label='Volume')
    ax2.tick_params(axis='y', labelcolor=color_volume)
    ax2.legend(loc='upper right')

    fig.tight_layout()  # Pour s'assurer qu'il n'y ait pas de chevauchement
    plt.title('Cours d\'ouverture et de clôture en fonction des dates')
    plt.grid(True)
    plt.show()