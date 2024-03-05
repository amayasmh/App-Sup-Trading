import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np

# Chargement des données
dataframe = pd.read_csv("./Files/CAC40_historique_2024-03-05 22:17:22.310508.csv")
features = dataframe[['open', 'high', 'low', 'close', 'volume']].values

# Préparation des données
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_features = scaler.fit_transform(features)

# Création des séquences
def create_sequences(data, sequence_length=20):
    X, y = [], []
    for i in range(len(data) - sequence_length):
        X.append(data[i:i+sequence_length].flatten())  # Aplatir les données de la fenêtre
        y.append(data[i+sequence_length, 3])  # 'close' comme cible
    return np.array(X), np.array(y)

sequence_length = 20
X, y = create_sequences(scaled_features, sequence_length)

# Division des données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Construction et entraînement du modèle de régression linéaire
model = LinearRegression()
model.fit(X_train, y_train)

# Prédiction pour les prochains pas
def predict_future_prices(model, last_sequence, n_future_steps=5):
    future_prices = []
    current_sequence = last_sequence

    for _ in range(n_future_steps):
        next_price_scaled = model.predict(current_sequence.reshape(1, -1))[0]
        future_prices.append(next_price_scaled)
        
        # Mise à jour de la séquence avec la prédiction (en décalant et en ajoutant la prédiction à la fin)
        current_sequence = np.roll(current_sequence, -5)
        current_sequence[-5:] = next_price_scaled  # Simulez l'ajout de nouvelles caractéristiques basées sur la prédiction

    # Inversez la normalisation pour les prix futurs
    # NOTE : Cette partie peut nécessiter des ajustements en fonction de votre méthode de normalisation et de vos données
    future_prices = np.array(future_prices).reshape(-1, 1)
    dummy_features = np.zeros((len(future_prices), scaled_features.shape[1] - 1))
    inverse_transform_features = np.concatenate((dummy_features, future_prices), axis=1)
    future_prices_real = scaler.inverse_transform(inverse_transform_features)[:, -1]
    
    return future_prices_real

# Utilisez la dernière séquence de X_test comme base pour les prédictions futures
last_sequence = X_test[-1]

# Prédire les prix futurs
n_future_steps = 5
future_prices = predict_future_prices(model, last_sequence, n_future_steps)
print(f"Les prix prédits pour les {n_future_steps} prochains intervalles sont: {future_prices}")


# Prédiction et évaluation
predicted = model.predict(X_test)
mse = mean_squared_error(y_test, predicted)
print(f"Erreur quadratique moyenne (MSE): {mse}")

# Affichage des résultats
true_prices = scaler.inverse_transform(np.concatenate((X_test[:, -4:-1], y_test.reshape(-1, 1), X_test[:, -1:]), axis=1))[:, 3]
predicted_prices = scaler.inverse_transform(np.concatenate((X_test[:, -4:-1], predicted.reshape(-1, 1), X_test[:, -1:]), axis=1))[:, 3]

plt.figure(figsize=(14, 5))
plt.plot(true_prices, label='Vrai Prix')
plt.plot(predicted_prices, label='Prix Prédit')
plt.title('Prédiction du Prix de l\'Action avec Régression Linéaire')
plt.xlabel('Temps')
plt.ylabel('Prix de l\'Action')
plt.legend()
plt.show()
