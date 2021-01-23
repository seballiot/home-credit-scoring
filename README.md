# Projet banque et modèle de Scoring

L'objectif de ce projet est de réaliser un modèle de machine learning sur des données bancaires de bout en bout, jusqu’à sa mise en production.

### Groupe 1

- AMROUCHE Belkacem
- ALLIOT Sébastien
- BENKANIA Mustapha
- DANI Sofian

### Composition du repository

`machine_learning_scripts/` : scripts de nettoyage, analyse et modélisation

`web_app_flask/` : Application Web développée en Flask

### Running de l'application Web

- Aller dans le dossier dédié
```
cd web_app_flask/
```
- Création d'un "virtual environment"
```
python3 -m venv venv-banque
# Si python3 non reconnu, essayer avec 'python'
```
- On rentre dans l'environnement virtuel
```
#  Sur Unix et MacOS
source venv-banque/bin/activate

# Sur Windows
venv-banque\Scripts\activate.bat
```
- Mise à jour pip
```
pip install --upgrade pip
```
- Installation des dépendances (dans le virtual env)
```
pip install -r requirements.txt
```
- Variable global
```
#  Sur Unix et MacOS
export FLASK_APP=projectapp.py

# Sur Windows
set FLASK_APP=projectapp.py
```
- Running du projet
```
flask run
```
NB : kill le serveur + sortir de l'environnement virtuel 
```
CTRL C

deactivate
```
