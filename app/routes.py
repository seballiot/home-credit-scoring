from flask import render_template, request, redirect, url_for, Markup, session
from app import app, db
from app.models import *


@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('accueil'))

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

    age_range = db.engine.execute('SELECT AGE_IN_YEARS_RANGE, COUNT(SK_ID_CURR) as total '
                                  'FROM application_train_enhanced '
                                  'GROUP BY AGE_IN_YEARS_RANGE;')
    for age in age_range:
        if age['AGE_IN_YEARS_RANGE'] == 1:
            nb_age_a = age['total']
        elif age['AGE_IN_YEARS_RANGE'] == 2:
            nb_age_b = age['total']
        elif age['AGE_IN_YEARS_RANGE'] == 3:
            nb_age_c = age['total']
        elif age['AGE_IN_YEARS_RANGE'] == 4:
            nb_age_d = age['total']

    return render_template(
        'dashboard.html',
        labels=labels,
        data=data,
        nb_client_homme=nb_client_homme,
        nb_client_femme=nb_client_femme,
        nb_client_na=nb_client_na,
        nb_age_a=nb_age_a,
        nb_age_b=nb_age_b,
        nb_age_c=nb_age_c,
        nb_age_d=nb_age_d,
        page='dashboard'
    )


@app.route('/clients/<string:base>', methods=['GET'], defaults={"page": 1, "error": None})
@app.route('/clients/<string:base>/p/<int:page>', methods=['GET'], defaults={"error": None})
@app.route('/clients/<string:base>/<int:error>', methods=['GET'], defaults={"page": 1})
def clients(page, error, base):
    if 'username' not in session:
        return redirect(url_for('accueil'))
    page = page
    per_page = 20

    if base == "train":
        liste_clients = ApplicationTrain.query.paginate(page, per_page, error_out=False)
        nb_clients = ApplicationTrain.query.count()
    elif base == "test":
        liste_clients = ApplicationTest.query.paginate(page, per_page, error_out=False)
        nb_clients = ApplicationTest.query.count()

    return render_template(
        'clients.html',
        clients=liste_clients,
        per_page=20,
        nb_clients=nb_clients,
        page='clients',
        base=base,
        id_error=error
    )


@app.route('/client/<int:id>', methods=['GET'])
def get_client(id):
    if 'username' not in session:
        return redirect(url_for('accueil'))
    id = Markup.escape(id)

    client_train = db.engine.execute('SELECT * FROM application_train WHERE SK_ID_CURR = '+id+';')
    client_train = client_train.fetchone()

    client_test = db.engine.execute('SELECT * FROM application_test WHERE SK_ID_CURR = ' + id + ';')
    client_test = client_test.fetchone()

    if client_train is None and client_test is None:
        return redirect(url_for('clients', base = "train", error=id))
    else:

        client_type = "train" if client_test is None else "test";

        if client_test is None:
            client = client_train
            client_data_enhanced = db.engine.execute('SELECT * FROM application_train_enhanced WHERE SK_ID_CURR = ' + id + ';')

            moy_revenu = db.engine.execute('SELECT AVG(AMT_INCOME_TOTAL) as moy_revenu FROM application_train;')
            moy_revenu = round(moy_revenu.fetchone()['moy_revenu'], 2)
            perc_ecart = round((client.AMT_INCOME_TOTAL - moy_revenu) / moy_revenu * 100)

            moy_enquiries = db.engine.execute('SELECT AVG(TOTAL_AMT_REQ_CREDIT_BUREAU) AS moy_enquiries '
                                              'FROM application_train_enhanced;')
            moy_enquiries = round(moy_enquiries.fetchone()['moy_enquiries'], 1)

        else:
            client = client_test
            client_data_enhanced = db.engine.execute('SELECT * FROM predictions WHERE SK_ID_CURR = ' + id + ';')

            moy_revenu = db.engine.execute('SELECT AVG(AMT_INCOME_TOTAL) as moy_revenu FROM application_test;')
            moy_revenu = round(moy_revenu.fetchone()['moy_revenu'], 2)
            perc_ecart = round((client.AMT_INCOME_TOTAL - moy_revenu) / moy_revenu * 100)

            moy_enquiries = db.engine.execute('SELECT AVG(TOTAL_AMT_REQ_CREDIT_BUREAU) AS moy_enquiries '
                                              'FROM predictions;')
            moy_enquiries = round(moy_enquiries.fetchone()['moy_enquiries'], 1)

        return render_template(
            'client.html',
            client=client,
            client_data_enhanced=client_data_enhanced.fetchone(),
            page='client',
            moy_revenu=moy_revenu,
            perc_ecart=perc_ecart,
            moy_enquiries=moy_enquiries,
            client_type=client_type
        )


@app.route('/post_client/', methods=['POST'])
def post_client():
    if 'username' not in session:
        return redirect(url_for('accueil'))
    return redirect(url_for('get_client', id=request.form['id']))


@app.route('/', methods=['GET'])
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
    userpost = Markup.escape(request.form ['username'])
    mdppost = Markup.escape(request.form ['mdp'])

    utilisateur = db.engine.execute('SELECT username, mdp '
                                    'FROM users')
    user=utilisateur.fetchall()
    for x in user:
        if userpost == x[0] and mdppost == x[1]:
            session['username'] = x[0]
            return redirect(url_for('dashboard'))

    else:
        return redirect(url_for('accueil'))


@app.route('/deconnexion', methods=['GET'])
def deconnexion():
    session.pop('username', None)
    return redirect(url_for('accueil'))


@app.route('/super_connex', methods=['POST'])
def super_connex():

    userpost = Markup.escape(request.form ['username'])
    mdppost = Markup.escape(request.form ['mdp'])

    utilisateur = db.engine.execute('SELECT username, mdp '
                                    'FROM super_admin')
    user=utilisateur.fetchall()
    for x in user:
        if userpost == x[0] and mdppost == x[1]:
            session['username'] = "Admin"
            return redirect(url_for('dashboard'))

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
    if 'username' not in session or session['username'] != "Admin":
        return redirect(url_for('dashboard'))

    users_temp = db.engine.execute('SELECT * FROM users_temp')

    return render_template(
        'users_temp.html',
        users_temp=users_temp
    )


@app.route('/users', methods=['GET'])
def users():
    if 'username' not in session or session['username'] != "Admin":
        return redirect(url_for('dashboard'))

    users = db.engine.execute('SELECT * FROM users')

    return render_template(
        'users.html',
        users=users
    )


@app.route('/delete/<int:id>/', methods=['GET'])
def delete(id):
    if 'username' not in session or session['username'] != "Admin":
        return redirect(url_for('dashboard'))

    db.engine.execute('DELETE FROM users WHERE id = "'+str(Markup.escape(id))+'";')
    return redirect(url_for('users'))


@app.route('/validate/<int:id>/<string:username>/<string:mdp>/<string:mail>', methods=['GET'])
def validate(id,username,mdp,mail):
    if 'username' not in session or session['username'] != "Admin":
        return redirect(url_for('dashboard'))

    db.engine.execute('INSERT INTO users (username, mdp, mail) VALUES ("'+username+'", "'+mdp+'", "'+mail+'")')
    db.engine.execute('DELETE FROM users_temp WHERE id = "'+str(id)+'";')
    return redirect(url_for('get_users_temp'))


@app.route('/refused/<int:id>/', methods=['GET'])
def refused(id):
    if 'username' not in session or session['username'] != "Admin":
        return redirect(url_for('dashboard'))

    db.engine.execute('DELETE FROM users_temp WHERE id = "'+str(Markup.escape(id))+'";')
    return redirect(url_for('get_users_temp'))