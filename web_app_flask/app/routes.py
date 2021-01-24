from flask import render_template, request, redirect
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
                               'LIMIT 5;')

    # Formatage pour l'affichage avec graph.js
    labels = "["
    data = "["
    for one in top_client_nb_credit:
        labels += "#"+str(one.SK_ID_CURR)+","
        data += str(one.nb_client)+","
    labels = labels[:-1]+"]"
    data = data[:-1] + "]"

    return render_template(
        'dashboard.html',
        labels=labels,
        data=data
    )