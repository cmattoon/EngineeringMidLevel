from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, IntegerField, DateField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class LoginForm(Form):
    """ For /login """
    openid = StringField('openid', validators=[DataRequired])
    remember_me = BooleanField('remember_me', default=False)


class FeatureRequest(Form):
    title = StringField('feature_name',
                        validators=[DataRequired])

    description = TextAreaField('description',
                              validators=[DataRequired])
    
    client_priority = IntegerField('priority')
    """
    Problem: Setting priority from FeatureRequest form
    requires the user to know the integer value, or involves
    a more complex UI, then inserting and readjusting the 
    IDs of all the other ones (e.g., this is new priority #1)
    
    Idea: Set priority here "high, med, low", which
    is then sorted by "hi-med-low, date_entered", then user can
    refine value with draggable datatable or something clever.
    """
    target_date = DateField('target_date',
                            validators=[DataRequired])
    ticket_url = StringField('ticket_url', 
                             validators=[DataRequired])

    product_area = SelectField('product_area_id', choices=[
            (1, 'Policies'),
            (2, 'Billing'),
            (3, 'Claims'),
            (4, 'Reports')
            ])

    client = SelectField('client_id', choices=[
            (1, 'Client1'),
            (2, 'Client2'),
            (3, 'Client3'),
            ])
        
    submit = SubmitField('Create')
