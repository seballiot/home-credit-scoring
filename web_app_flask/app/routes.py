from flask import render_template, request, redirect, url_for, Markup
from app import app, db
from app.models import *


@app.route('/test', methods=['GET'], defaults={"page": 1})
@app.route('/test<int:page>', methods=['GET'])
def homepage(page):
    page = page
    per_page = 10
    content = HomeCreditColumnsDescription.query.paginate(page, per_page, error_out=False)
    return render_template('index.html', content=content)


@app.route('/', methods=['GET'])
def dashboard():

    top_client_nb_credit = db.engine.execute('SELECT SK_ID_CURR, count(*) AS nb_client '
                                             'FROM bureau '
                                             'GROUP BY SK_ID_CURR '
                                             'ORDER BY nb_client DESC '
                                             'LIMIT 10;')
    # Formatage du resultat pour l'affichage du graph
    labels = "["
    data = "["
    for one in top_client_nb_credit:
        labels += "#" + str(one.SK_ID_CURR) + ","
        data += str(one.nb_client) + ","
    labels = labels[:-1] + "]"
    data = data[:-1] + "]"

    client_gender = db.engine.execute('SELECT CODE_GENDER, COUNT(DISTINCT SK_ID_CURR) as total '
                                      'FROM application_train '
                                      'GROUP BY CODE_GENDER;')
    # Formatage du resultat pour l'affichage du graph
    for gender in client_gender:
        if gender['CODE_GENDER'] == "M":
            nb_client_homme = gender['total']
        elif gender['CODE_GENDER'] == "F":
            nb_client_femme = gender['total']
        else:
            nb_client_na = gender['total']

    return render_template(
        'dashboard.html',
        labels=labels,

        data=data,
        nb_client_homme=nb_client_homme,
        nb_client_femme=nb_client_femme,
        nb_client_na=nb_client_na,
        page='dashboard'
    )


@app.route('/clients', methods=['GET'], defaults={"page": 1})
@app.route('/clients/<int:page>', methods=['GET'])
def clients(page):
    page = page
    per_page = 20
    liste_clients = ApplicationTrain.query.paginate(page, per_page, error_out=False)
    nb_clients = ApplicationTrain.query.count()

    print(nb_clients);

    return render_template(
        'clients.html',
        clients=liste_clients,
        per_page=20,
        nb_clients=nb_clients,
        page='clients'
    )


@app.route('/client/<int:id>', methods=['GET'])
def get_client(id):
    id = Markup.escape(id)

    client = db.engine.execute('SELECT * FROM application_train WHERE SK_ID_CURR = '+id+';')
    client = client.fetchone()

    client_data_enhanced = db.engine.execute('SELECT * FROM application_train_enhanced WHERE SK_ID_CURR = ' + id + ';')

    moy_revenu = db.engine.execute('SELECT AVG(AMT_INCOME_TOTAL) as moy_revenu FROM application_train;')
    moy_revenu = round(moy_revenu.fetchone()['moy_revenu'], 2)
    perc_ecart = round((client.AMT_INCOME_TOTAL - moy_revenu) / moy_revenu * 100)

    moy_enquiries = db.engine.execute('SELECT AVG(TOTAL_AMT_REQ_CREDIT_BUREAU) as moy_enquiries FROM application_train_enhanced;')
    moy_enquiries = round(moy_enquiries.fetchone()['moy_enquiries'], 1)

    return render_template(
            'client.html',
            client=client,
            client_data_enhanced=client_data_enhanced.fetchone(),
            page='client',
            moy_revenu=moy_revenu,
            perc_ecart=perc_ecart,
            moy_enquiries=moy_enquiries
        )


@app.route('/post_client/', methods=['POST'])
def post_client():
    return redirect(url_for('get_client', id=request.form['id']))



@app.route('/accueil', methods=['GET'])
def accueil():
    return render_template('accueil.html')

@app.route('/super_admin', methods=['GET'])
def super_admin():
    return render_template('super_admin.html')

@app.route('/inscription', methods=['GET'])
def inscription():
    return render_template('inscription.html')

@app.route('/connexion', methods=['POST'])
def connexion():


    userpost = request.form ['username']
    mdppost = request.form ['mdp']

    utilisateur = db.engine.execute('SELECT username, mdp '
                                    'FROM users')
    user=utilisateur.fetchall()
    for x in user:
        if userpost == x[0] and mdppost == x[1]:
                return redirect(url_for('dashboard'))

    else:
        return redirect(url_for('accueil'))


@app.route('/super_connex', methods=['POST'])
def super_connex():

    userpost = request.form ['username']
    mdppost = request.form ['mdp']

    utilisateur = db.engine.execute('SELECT username, mdp '
                                    'FROM super_admin')
    user=utilisateur.fetchall()
    for x in user:
        if userpost == x[0] and mdppost == x[1]:
                return redirect(url_for('get_users_temp'))

    else:
        return redirect(url_for('super_admin'))

@app.route('/create', methods=['POST'])
def create():


    userpost = request.form ['username']
    mdppost = request.form ['mdp']
    mailpost = request.form['email']

    db.engine.execute('INSERT INTO users_temp (username, mdp, mail) VALUES ("'+userpost+'", "'+mdppost+'", "'+mailpost+'")')

    return render_template('accueil.html')

@app.route('/users_temp', methods=['GET'])
def get_users_temp():
    users_temp = db.engine.execute('SELECT * FROM users_temp')

    return render_template(
        'users_temp.html',
        users_temp=users_temp
    )

@app.route('/users', methods=['GET'])
def users():
    users = db.engine.execute('SELECT * FROM users')

    return render_template(
        'users.html',
        users=users
    )

@app.route('/delete/<int:id>/', methods=['GET'])
def delete(id):
    db.engine.execute('DELETE FROM users WHERE id = "'+str(id)+'";')
    return redirect(url_for('users'))

@app.route('/validate/<int:id>/<string:username>/<string:mdp>/<string:mail>', methods=['GET'])
def validate(id,username,mdp,mail):
    db.engine.execute('INSERT INTO users (username, mdp, mail) VALUES ("'+username+'", "'+mdp+'", "'+mail+'")')
    db.engine.execute('DELETE FROM users_temp WHERE id = "'+str(id)+'";')
    return redirect(url_for('get_users_temp'))

@app.route('/refused/<int:id>/', methods=['GET'])
def refused(id):
    db.engine.execute('DELETE FROM users_temp WHERE id = "'+str(id)+'";')
    return redirect(url_for('get_users_temp'))