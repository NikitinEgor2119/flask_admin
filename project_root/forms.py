from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired

class UserForm(FlaskForm):
    balance = FloatField("Balance", validators=[DataRequired()])
    commission_rate = FloatField("Commission Rate", validators=[DataRequired()])
    webhook_url = StringField("Webhook URL")
    role = SelectField("Role", choices=[("admin", "Admin"), ("user", "User")])
    submit = SubmitField("Submit")


class TransactionForm(FlaskForm):
    amount = FloatField("Amount", validators=[DataRequired()])
    status = SelectField("Status", choices=[("waiting", "Waiting"), ("confirmed", "Confirmed"), ("cancelled", "Cancelled"), ("expired", "Expired")])
    submit = SubmitField("Submit")