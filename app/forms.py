from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, IntegerField, DateField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from app import db, models

class LoginForm(Form):
    """ For /login """
    openid = StringField('openid', validators=[DataRequired])
    remember_me = BooleanField('remember_me', default=False)


class FeatureRequestForm(Form):
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

    product_area = SelectField('product_area_id', choices=[])

    client = SelectField('client_id', choices=[])
        
    submit = SubmitField('Create')

    def __init__(self):
        """I'm not sure this is the best way to go about this. 
        Dynamic options could also be easily handled via KO
        """
        super(FeatureRequestForm, self).__init__()
        self.product_area.choices = self.getProductAreas()
        self.client.choices = self.getClients()


    def getProductAreas(self):
        """If this changes often, it might be worth storing in a table.
        For now, I'll just keep this here and store the value as a string.
        
        Returns:
            a list of strings (product area names)
        """
        areas = [(1,'Policies'), (2,'Billing'), (3,'Claims'), (4,'Reports')]
        sorted(areas)
        return areas

    def getClients(self):
        """Clients should probably be in a table for sure, if for no
        other reason than there's likely other useful info to store
        in that table. Alternatively, this might use an API call to
        an in-house CRM system or something to avoid extra work in
        keeping the list up-to-date.
        
        Returns:
            a list of tuples (int(id), str(name))
        """
        clients = []
        for client in models.Client.query.all():
            clients.append( (int(client.id), str(client.name)) )
        return clients
                           
