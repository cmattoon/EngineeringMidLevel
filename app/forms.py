from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
    """ For /login """
    openid = StringField('openid', validators=[DataRequired])
    remember_me = BooleanField('remember_me', default=False)


class FeatureRequest(Form):
    title = StringField('feature_name',
                        validators=[DataRequired])
    description = StringField('description',
                              validators=[DataRequired])
    #client_id = DropDown()
    #client_priority = Integer
    #target_date = Date
    ticket_url = StringField('ticket_url', validators=[DataRequired])
    #product_area = StringField('product_area')
    #attachments
