import wtforms.validators
from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.simple import StringField, HiddenField
from wtforms.fields import SelectField, BooleanField
from wtforms.validators import DataRequired, Length, InputRequired


class addDevice(FlaskForm):
	mac_address = StringField("Mac Address", validators=[DataRequired(), Length(max=17)])
	employee = SelectField("Employee", coerce=int, validators=[InputRequired()])
	enabled = BooleanField('Enabled')
	device_id = HiddenField()
	submit = SubmitField('Save')


class permissionForm(FlaskForm):
	permission = SelectField(label=None, choices=[("normal", "Normal"), ("privileged", "Privileged")])
	submit = SubmitField('Edit Permissions')
