from app import db

class User(db.Model):
    """Represents a User, obviously"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)

    def __repr__(self):
        """ For debugging """
        return '<User %r>' % (self.username)
