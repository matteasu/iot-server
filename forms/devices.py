from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.fields.simple import StringField
from wtforms.fields import SelectField, BooleanField
from wtforms.validators import DataRequired, Length, InputRequired


class addDevice(FlaskForm):
	mac_address = StringField("Mac Address", validators=[DataRequired(), Length(max=17)])
	employee = SelectField("Employee", coerce=int, validators=[InputRequired()])
	enabled = BooleanField('Enabled', validators=[DataRequired()])
