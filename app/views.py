import datetime
from flask import render_template, flash, redirect, jsonify, request, abort
from app import app, db, models
from .forms import LoginForm, FeatureRequestForm



@app.errorhandler(404)
def err_not_found(err):
    return render_template('404.html'), 404

@app.errorhandler(500)
def err_internal_server(err):
    return render_template('500.html'), 500

def get_product_areas():
    """ Depending on how often this changes, it might be worth putting
    in a DB table. For now, I'll just return a list and store the value
    as a string.

    Returns:
        a list of product areas
    """
    areas = ['Policies', 'Billing', 'Claims', 'Reports']
    sort(areas) # Unless this is undesirable
    return areas

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Guest'}
    return render_template('index.html',
                           title='Home',
                           user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')

    return render_template('login.html',
                           title='Login',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])


@app.route('/feature', methods=['GET', 'POST'])
def feature():
    """Shows feature request form.
    If id is provided in GET, treat it as an edit form.
    """
    form = FeatureRequestForm()
    
    if form.validate_on_submit():
        flash('Uh..........')

    return render_template('feature.html',
                           title='Feature Request',
                           form=form)

@app.route('/feature/<int:id>')
def view_feature(id):
    form = FeatureRequestForm()
    return render_template('feature.html', title='Edit Feature', form=form)

"""
----------------------------------------------------------------
----------------------------------------------------------------
These are the "API" methods, to demonstrate a decoupled app

/client will take you to the KO.js client UI




----------------------------------------------------------------
----------------------------------------------------------------
"""
@app.route('/client')
def client():
    """This route corresponds to a single-page API client
    using Knockout.js
    """
    return render_template('client.html')

@app.route('/api/features')
def api_features():
    """ API method to return a list of all existing features.
    """
    return jsonify([req.toJSON() for req in 
            models.FeatureRequest.query.all()])

@app.route('/api/feature', methods=['POST'])
def api_feature_add():
    if not request.json or not 'title' in request.json:
        abort(400)
    data = request.json

    # Please upgrade to Enterprise edition for server-side
    # validation of `data`
    fr = models.FeatureRequest(
        title=data.get('title', ''),
        description=data.get('description', ''),
        client_id=data.get('client_id', 0),
        product_area=data.get('product_area', ''),
        client_priority=data.get('client_priority', 0),
        date_entered=datetime.datetime.now(),
        target_date=data.get('target_date'),
        ticket_url=data.get('uri')
        )

    db.session.add(fr)
    db.session.commit()

    return jsonify(request.json)

@app.route('/api/clients', methods=['GET'])
def api_clients():
    """Returns a list of all available clients for the 
    selectbox.
    """
    return jsonify([client.toJSON() for client in 
                    models.Client.query.all()])
