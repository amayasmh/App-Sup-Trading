# App-Sup-Trading

## Introduction

Le projet App-Sup-Trading est une initiative visant à développer une solution d'automatisation, appelée Robotic Process Automation (RPA), pour la collecte régulière des cours de certaines actions du CAC 40. L'objectif principal est de construire une base de données robuste pour l'entraînement d'un algorithme de trading haute fréquence. Ce projet est structuré en quatre étapes principales, allant de l'acquisition des données historiques à la surveillance en temps réel du marché boursier. Notre solution intègre un robot conçu pour mettre à jour la base de données en temps réel, ainsi qu'une application en ligne de commande qui permet de suivre en temps réel ou d'accéder à l'historique des actions.

## Robot d'Extraction de Données de Marché Financier

### Introduction

Ce document technique détaille le fonctionnement d'un robot automatisé conçu pour extraire et stocker les données financières en temps réel des marchés boursiers, en particulier celles liées au CAC40, grâce à l'utilisation de la bibliothèque yfinance. Le script Python développé pour cette tâche interagit avec une base de données PostgreSQL pour gérer les données recueillies. Ce processus inclut la création de tables de base de données, l'insertion des données en temps réel, et le suivi des opérations via des fichiers de log.

### Structure du Robot

Le robot est structuré autour de plusieurs modules principaux, chacun ayant une fonction spécifique :

- **Modules.DataBaseFuncs** : Contient les fonctions pour se connecter à la base de données PostgreSQL, créer des tables, des déclencheurs et insérer des données.
- **Modules.Data** : Fournit les fonctions pour extraire les données financières en temps réel.
- **Modules.Symbols** : Répertorie les symboles des actions à surveiller.

### Flux de Travail du Robot

1. **Initialisation de la Connexion à la Base de Données** : Le robot établit d'abord une connexion à la base de données PostgreSQL en utilisant les paramètres de configuration stockés dans `./Config/Config.json`.
2. **Création de Tables et de Triggers** : Le robot vérifie l'existence des tables nécessaires (`cac40_daily_data`, `cac40_history_data`) et crée un déclencheur pour copier automatiquement les nouvelles insertions de `cac40_daily_data` vers `cac40_history_data`.
3. **Extraction des Données** : Le robot exécute une boucle continue durant les heures de trading (de 09:00 à 17:30), utilisant `yfinance` pour récupérer les données en temps réel pour chaque symbole configuré.
4. **Stockage des Données** : Les données extraites sont ensuite insérées dans la table `cac40_daily_data`. Un déclencheur configuré copie automatiquement ces données dans `cac40_history_data` pour un archivage à long terme.
5. **Gestion des Logs** : Toutes les opérations importantes sont enregistrées dans un fichier log pour faciliter le débogage et le suivi des performances.

### Configuration et Dépendances

- **PostgreSQL** et **Python 3.x** comme base technologique.
- **Bibliothèques Python** nécessaires : `json`, `psycopg2`, `pandas`, `yfinance`, ainsi que `datetime` et `time` pour la gestion temporelle.
- **Configuration JSON** : Contient les paramètres de connexion à la base de données.

## Application en Ligne de Commande Sup-Trading

### Introduction

L'application en ligne de commande Sup-Trading offre une interface utilisateur pour interagir avec les données du marché boursier en temps réel et historique. Elle permet de suivre le cours des actions, de visualiser l'historique des actions, d'afficher les symboles des actions, et plus encore.

### Fonctionnalités de l'Application

- **Menu Principal** : Propose les options suivantes à l'utilisateur :
  - **Suivre le cours des actions en temps réel** : Pour le suivi actuel des actions du CAC40 et d'autres marchés.
  - **Afficher l'historique des actions** : Pour consulter l'historique des prix des actions pour une période ou une date spécifique.
  - **Afficher les symboles des actions** : Pour afficher une liste des symboles boursiers disponibles.
  - **Quitter** : Pour terminer l'exécution de l'application.

### Structure et Modules du Programme

L'application se compose de plusieurs modules, chacun responsable d'une fonctionnalité spécifique :

- **Modules Principaux** : Gèrent l'affichage du menu, le traitement des choix de l'utilisateur, et l'interaction avec d'autres modules.
- **Module Data** : S'occupe de l'extraction des données historiques et en temps réel en utilisant `yfinance`.
- **Module Save** : Permet de sauvegarder les données extraites dans des fichiers CSV ou Excel.
- **Module Viz** : Utilise `matplotlib` pour créer des graphiques représentant l'historique des actions.

### Gestion des Logs

L'application utilise le module `logging` pour enregistrer les événements clés, facilitant ainsi le débogage et le suivi efficace de son utilisation.




# Guide de Configuration Technique pour App-Sup-Trading

Ce guide détaille les étapes nécessaires au déploiement de la solution App-Sup-Trading, y compris la préparation de l'environnement, l'installation des dépendances, et le lancement de l'application.

## Prérequis

- Python 3.x installé sur votre machine.
- Accès à un serveur PostgreSQL.

## Étapes de Configuration

### 1. Récupération du Projet

Clonez ou téléchargez le dossier du projet depuis son dépôt Git vers un répertoire de votre choix :

```bash
git clone URL_DU_PROJET
```

### 2. Création et Activation d'un Environnement Virtuel

Dans le dossier du projet, créez un environnement virtuel nommé `env` :

```bash
python -m venv env
```

Activez cet environnement virtuel :

- Sous Windows :

  ```cmd
  .\env\Scripts\activate
  ```

- Sous macOS et Linux :

  ```bash
  source env/bin/activate
  ```

### 3. Installation des Dépendances

Avec l'environnement activé, installez les dépendances nécessaires via :

```bash
pip install -r requirements.txt
```

Assurez-vous que `requirements.txt` est présent à la racine du projet.

### 4. Préparation des Dossiers

- **Dossier Files** : Créez un dossier `Files` à la racine pour les fichiers générés :

  ```bash
  mkdir Files
  ```

- **Dossier Log** : Créez un dossier `Log` pour les fichiers de journalisation :

  ```bash
  mkdir Log
  ```

### 5. Configuration de la Base de Données

Modifiez le fichier de configuration (typiquement `Config.json` dans le dossier `Config`) avec les paramètres de votre base de données PostgreSQL :

```json
{
  "host": "Votre_Hôte",
  "database": "Nom_De_La_Base_De_Données",
  "user": "Votre_Utilisateur",
  "password": "Votre_Mot_De_Passe"
}
```

### 6. Lancement de l'Application

Avec l'environnement toujours activé, lancez l'application via :

- Sous Windows :

  ```cmd
  python Main.py
  ```

- Sous macOS et Linux :

  ```bash
  python3 Main.py
  ```

Vous verrez alors le menu principal de l'application, prêt à être utilisé.

## Conclusion

Suivez ce guide pour configurer et démarrer la solution App-Sup-Trading sur votre système. Cette configuration de base vous permettra de lancer l'application et d'accéder à ses fonctionnalités.