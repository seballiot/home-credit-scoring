# Home Credit Scoring 

Groupe 1
 

### Install et Run

- Création d'un "virtual environment"
```
python3 -m venv venv-banque
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
export FLASK_APP=projectapp.py
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