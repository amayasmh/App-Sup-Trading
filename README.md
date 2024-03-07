# App-Sup-Trading

## Introduction

Le projet App-Sup-Trading est une initiative visant à développer une solution d'automatisation, appelée Robotic Process Automation (RPA), pour la collecte régulière des cours de certaines actions du CAC 40. L'objectif principal est de construire une base de données robuste pour l'entraînement d'un algorithme de trading haute fréquence. Ce projet est structuré en quatre étapes principales, allant de l'acquisition des données historiques à la surveillance en temps réel du marché boursier. Notre solution intègre un robot conçu pour mettre à jour la base de données en temps réel, ainsi qu'une application en ligne de commande qui permet de suivre en temps réel ou d'accéder à l'historique des actions.

## Robot d'Extraction de Données de Marché Financier

### Introduction

Ce document technique détaille le fonctionnement d'un robot automatisé conçu pour extraire et stocker les données financières en temps réel des marchés boursiers, en particulier celles liées au CAC40, grâce à l'utilisation de la bibliothèque yfinance. Le script Python développé pour cette tâche interagit avec une base de données PostgreSQL pour gérer les données recueillies. Ce processus inclut la création de tables de base de données, l'insertion des données en temps réel, et le suivi des opérations via des fichiers de log.

### Structure du Robot


Le robot est constitué de plusieurs modules clés, chacun dédié à une tâche spécifique :

- **Modules.DataBaseFuncs** : Ce module inclut les fonctions nécessaires pour établir une connexion avec la base de données PostgreSQL, créer des tables et des déclencheurs, et pour l'insertion des données.
- **Modules.Data** : Fournit les fonctions pour l'extraction des données financières en temps réel via la bibliothèque yfinance.
- **Modules.Symbols** : Contient la liste des symboles boursiers du CAC40 à surveiller.
- **Modules.SendMail** : Gère l'envoi d'emails avec les fichiers de données extraits.

## Flux de Travail du Robot

Le robot suit un processus structuré pour extraire, stocker et gérer les données financières en temps réel. Chaque étape du processus est conçue pour fonctionner de manière autonome et efficace :

1. **Connexion à la Base de Données** :
   - Initie la connexion à PostgreSQL en utilisant les paramètres définis dans `./Config/DBConfig.json`.
   - Cette connexion permet au robot d'interagir directement avec la base de données pour toutes les opérations nécessaires.

2. **Création de Tables et Déclencheurs** :
   - Vérifie l'existence et crée, si nécessaire, deux tables principales : `cac40_daily_data` pour les données du jour et `cac40_history_data` pour l'archivage.
   - Installe un déclencheur pour copier automatiquement chaque nouvelle entrée de `cac40_daily_data` vers `cac40_history_data`, assurant un archivage systématique des données.

3. **Extraction des Données** :
   - Lance une boucle d'extraction durant les heures de marché (09:00 à 17:30) pour récupérer les données des symboles listés dans `Modules.Symbols`.
   - Utilise `yfinance` pour obtenir des données financières précises et à jour.

4. **Insertion des Données dans la Table Daily** :
   - Insère les nouvelles données récupérées dans la table `cac40_daily_data`.
   - Le déclencheur configuré précédemment copie ces mêmes données dans `cac40_history_data` pour un stockage à long terme.

5. **Exportation des Données et Envoi par Email** :
   - À 17h55, compile toutes les données du jour de `cac40_daily_data` dans un fichier CSV.
   - Envoie ce fichier par email à une liste de destinataires prédéfinie, facilitant la diffusion rapide des informations.

6. **Nettoyage de la Table Daily** :
   - Vide la table `cac40_daily_data` avec une commande `TRUNCATE` après l'envoi de l'email, préparant ainsi la base de données pour la prochaine session de trading tout en conservant les archives dans `cac40_history_data`.

Ce flux de travail garantit une collecte et une gestion efficaces des données de marché, soutenant l'analyse et le trading en fournissant des données actualisées et archivées de manière fiable et accessible.


### Configuration et Dépendances

- **PostgreSQL** et **Python 3.x** comme base technologique.
- **Bibliothèques Python** nécessaires : `json`, `psycopg2`, `pandas`, `yfinance`, ainsi que `datetime` et `time` pour la gestion temporelle.
- **Configuration JSON** : Contient les paramètres de connexion à la base de données et la configuration du mail.



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
git clone git@github.com:amayasmh/App-Sup-Trading.git
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

### 5. Configuration de la Base de Données et de l'Email

#### Base de Données

Modifiez le fichier de configuration (typiquement `DBConfig.json` dans le dossier `Config`) avec les paramètres de votre base de données PostgreSQL :

```json
{
  "host": "Votre_Hôte",
  "database": "Nom_De_La_Base_De_Données",
  "user": "Votre_Utilisateur",
  "password": "Votre_Mot_De_Passe"
}
```

#### Email

Dans le même dossier `Config`, créez ou modifiez un fichier pour la configuration de l'email (vous pouvez l'appeler `MailConfig.json`) avec les paramètres suivants pour configurer le serveur SMTP et les destinataires des emails :

```json
{
    "host": "smtp.gmail.com",
    "port": 465,
    "user": "saghiraghiles.web@gmail.com",
    "password": "entg snoi szzo ymiz",
    "to": "aghiles.saghir@supdevinci-edu.fr,amayas.mahmoudi01@gmail.com"
}
```
### 6. Déploiement et Automatisation du robot

Le robot d'extraction de données peut être déployé et automatisé sur des systèmes Linux et Windows pour assurer son exécution pendant les heures de marché. Voici les étapes à suivre pour chaque système d'exploitation :

### Sur Linux (avec Cron)

1. **Ouvrir le Crontab :**
   - Ouvrez un terminal et tapez `crontab -e` pour éditer le fichier crontab de l'utilisateur actuel.

2. **Ajouter une Tâche Planifiée :**
   - Ajoutez la ligne suivante pour exécuter le script chaque jour ouvrable (du lundi au vendredi) pendant les heures de marché (09:00 à 17:30) :
     ```
     * 9-17 * * 1-5 /chemin/vers/python3 /chemin/vers/votre/script/Robot.py
     ```
   - Assurez-vous de remplacer `/chemin/vers/python3` et `/chemin/vers/votre/script/Robot.py` par les chemins réels vers votre interpréteur Python et votre script.

3. **Sauvegarder et Quitter :**
   - Sauvegardez les modifications et quittez l'éditeur. Le cron se chargera de lancer le script selon la planification définie.

### Sur Windows (avec Planificateur de Tâches)

1. **Ouvrir le Planificateur de Tâches :**
   - Appuyez sur `Win + R`, tapez `taskschd.msc` et appuyez sur `Entrée` pour ouvrir le Planificateur de Tâches.

2. **Créer une Nouvelle Tâche :**
   - Dans le menu `Action`, choisissez `Créer une tâche...`.
   - Donnez un nom à votre tâche, par exemple, `RobotExtractionDonnees`.

3. **Configurer les Triggers :**
   - Allez à l'onglet `Déclencheurs`, cliquez sur `Nouveau...` et configurez-le pour démarrer à 09:00 chaque jour ouvrable.

4. **Configurer l'Action :**
   - Allez à l'onglet `Actions`, cliquez sur `Nouveau...` et choisissez `Démarrer un programme`.
   - Dans `Programme/script`, indiquez le chemin vers votre interpréteur Python.
   - Dans `Ajouter des arguments`, entrez le chemin vers votre script, par exemple, `C:\chemin\vers\Robot.py`.
   - Dans `Démarrer dans`, spécifiez le répertoire de travail de votre script si nécessaire.

5. **Configurer les Conditions et Paramètres :**
   - Ajustez les onglets `Conditions` et `Paramètres` selon vos besoins, par exemple, pour ne pas exécuter la tâche si l'ordinateur fonctionne sur batterie.

6. **Sauvegarder la Tâche :**
   - Cliquez sur `OK` pour enregistrer votre tâche. Vous devrez peut-être fournir le mot de passe de votre compte utilisateur pour autoriser la planification de la tâche.

Votre robot est maintenant configuré pour s'exécuter automatiquement pendant les heures de marché sur Linux et Windows. Assurez-vous de tester la tâche planifiée pour vérifier qu'elle démarre comme prévu.


### 7. Lancement de l'Application de ligne de commande

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