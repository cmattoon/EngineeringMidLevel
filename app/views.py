from flask import render_template, flash, redirect
from app import app
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
    user = {'nickname': 'Buddy'}
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

@app.route('/admin/viewall')
def admin_viewall():
    """Show all feature requests"""
    return render_template('admin-viewall.html',
                           title='Admin - View All Requests')


@app.route('/admin/users')
def admin_users():
    """Show all users"""
    return render_template('admin-users.html',
                           title='Admin - All Users')

@app.route('/admin/clients')
def admin_clients():
    """Show all clients"""
    return render_template('admin-clients.html',
                           title='Admin - All Clients')

