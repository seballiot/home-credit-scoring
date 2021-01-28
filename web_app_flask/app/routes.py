from flask import render_template, request, redirect, url_for, Markup
from app import app, db
from app.models import *
import math


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

