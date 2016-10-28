from app import db

class User(db.Model):
    """Represents a User, obviously"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        """ For debugging """
        return '<User %r>' % (self.username)

class FeatureRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), index=True)
    description = db.Column(db.Text)
    client_id = db.Column(db.Integer)
    product_area_id = db.Column(db.Integer)
    client_priority = db.Column(db.Integer)
    date_entered = db.Column(db.DateTime)
    target_date = db.Column(db.DateTime)
    ticket_url = db.Column(db.Text)

    def __repr__(self):
        """ Debug """
        return '<FeatureRequest %s>' % (str(self.id))
