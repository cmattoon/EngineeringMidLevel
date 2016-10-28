from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm, FeatureRequest

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
    form = FeatureRequest()
    
    if form.validate_on_submit():
        flash('Uh..........')

    return render_template('feature.html',
                           title='Feature Request',
                           form=form)
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

