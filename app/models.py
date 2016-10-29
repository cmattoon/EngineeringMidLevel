import json
from datetime import datetime, date

from app import db

class AppModel:
    """Stolen from 
    http://stackoverflow.com/questions/7102754/jsonify-a-sqlalchemy-result-set-in-flask
    """
    __public__ = []

    def get_public(self, exclude=(), extra=()):
        "Returns model's PUBLIC data for jsonify"
        data = {}
        keys = self._sa_instance_state.attrs.items()
        public = self.__public__ + extra if self.__public__ else extra
        for k, field in keys:
            if public and k not in public: continue
            if k in exclude: continue
            value = self._serialize(field.value)
            if value:
                data[k] = value
        return data

    @classmethod
    def _serialize(cls, value, follow_fk=False):
        if type(value) in (datetime, date):
            ret = value.isoformat()
        elif hasattr(value, '__iter__'):
            ret = []
            for v in value:
                ret.append(cls._serialize(v))
        elif AppModel in value.__class__.__bases__:
            ret = value.get_public()
        else:
            ret = value

        return ret

class User(db.Model):
    """ Users, duh """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    requests = db.relationship('FeatureRequest', 
                               backref='author', lazy='dynamic')

    def __repr__(self):
        """ For debugging """
        return '<User %r>' % (self.username)

    def toJSON(self):
        return json.dumps(_to_json(self, self.__class__))

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
    def toJSON(self):
        return json.dumps(_to_json(self, self.__class__))

class FeatureRequest(db.Model, AppModel):
    """ Each row stores a Feature Request"""
    __public__ = ('id', 'user_id', 'title', 
                  'description', 'client_id',
                  'product_area', 'client_priority',
                  'date_entered', 'target_date',
                  'ticket_url', 'author', 'client')
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

    def toJSON(self):
        return {
            'id': self.id,
            'client': self.client.name,
            'title': self.title,
            'description': self.description,
            'client_id': self.client_id,
            'product_area': self.product_area,
            'client_priority': self.client_priority,
            }

