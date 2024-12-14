from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
    balance = DecimalField('Balance', validators=[DataRequired()])
    commission_rate = DecimalField('Commission Rate', validators=[DataRequired()])
    webhook_url = StringField('Webhook URL')
    role = SelectField('Role', choices=[('admin', 'Admin'), ('user', 'User')])
    submit = SubmitField('Submit')