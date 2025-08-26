# Espace Telmoudi - Plateforme Touristique

Une plateforme de gestion touristique pour l'Espace Telmoudi, permettant la gestion des avis, des rendez-vous et des comptes utilisateurs.

## Prérequis

- Python 3.8+ (déjà installé sur le PC cible)
- XAMPP (à installer)
- Les dépendances Python (déjà installées sur le PC cible)

## Installation de XAMPP

1. **Télécharger XAMPP**
   - Allez sur [le site officiel de XAMPP](https://www.apachefriends.org/download.html)
   - Téléchargez la version pour Windows
   - Exécutez le fichier d'installation téléchargé

2. **Installer XAMPP**
   - Double-cliquez sur le fichier d'installation
   - Suivez les instructions de l'assistant d'installation
   - Cochez au minimum "MySQL" et "phpMyAdmin" pendant l'installation
   - Notez le dossier d'installation (par défaut: `C:\xampp`)

3. **Démarrer les services**
   - Lancez le Panneau de Contrôle XAMPP
   - Démarrez les services "Apache" et "MySQL" en cliquant sur les boutons "Start"

## Configuration du projet

1. **Copier les fichiers**
   - Copiez le dossier du projet dans l'emplacement de votre choix sur le PC cible
   - Par exemple : `C:\Users\Utilisateur\Documents\plateforme-tourisme`

2. **Importer la base de données**
   - Ouvrez votre navigateur et allez à : http://localhost/phpmyadmin
   - Cliquez sur "Nouvelle base de données"
   - Entrez le nom : `espace_telmoudi`
   - Cliquez sur "Créer"
   - Sélectionnez la base de données nouvellement créée
   - Allez dans l'onglet "Importer"
   - Cliquez sur "Parcourir" et sélectionnez le fichier `database_backup.sql`
   - Cliquez sur "Exécuter" en bas de la page

3. **Vérifier la configuration de la base de données**
   - Ouvrez le fichier `db_config.py`
   - Vérifiez que les informations de connexion correspondent :
     ```python
     host="localhost"
     user="root"
     password=""  # Le mot de passe est vide par défaut avec XAMPP
     database="espace_telmoudi"
     ```

## Lancer l'application
2. **Naviguer vers le dossier du projet**
   ```
   cd C:\chemin\vers\votre\projet
   ```

3. **Démarrer l'application**
   ```
   python app.py
   ```

4. **Accéder à l'application**
   - Ouvrez un navigateur web
   - Allez à l'adresse : http://localhost:5000

## Structure du projet

- `app.py` - Point d'entrée de l'application
- `db_config.py` - Configuration de la base de données
- `templates/` - Fichiers de modèles HTML
- `static/` - Fichiers statiques (CSS, JS, images)
- `uploads/` - Dossier de stockage des fichiers téléversés

## Dépannage

- **Erreur de connexion à la base de données** :
  - Vérifiez que les services MySQL et Apache sont en cours d'exécution dans XAMPP
  - Vérifiez les informations de connexion dans `db_config.py`

- **Erreur de port** :
  - Si le port 5000 est déjà utilisé, vous pouvez le changer dans `app.py`
  - Modifiez la dernière ligne : `app.run(debug=True, port=5001)`

## Auteur

kabaw (nekthb rah )

    
# plateforme-tourisme
