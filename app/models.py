from app import db

class User(db.Model):
    """ Users, duh """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    requests = db.relationship('FeatureRequest', backref='author', lazy='dynamic')

    def __repr__(self):
        """ For debugging """
        return '<User %r>' % (self.username)

class Client(db.Model):
    """ This table should store a list of active clients.
    This is how the dropdown is populated.
    Needs admin interface, etc..
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    requests = db.relationship('FeatureRequest', backref='client', lazy='dynamic')
    # active = db.Column(db.Boolean)
    # created_by ...
    # created_on ...


class FeatureRequest(db.Model):
    """ Each row stores a Feature Request"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(255), index=True)
    description = db.Column(db.Text)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))    
    product_area = db.Column(db.String)
    client_priority = db.Column(db.Integer)
    date_entered = db.Column(db.DateTime)
    target_date = db.Column(db.DateTime)
    ticket_url = db.Column(db.Text)

    def __repr__(self):
        """ Debug """
        return '<FeatureRequest %s>' % (str(self.id))

