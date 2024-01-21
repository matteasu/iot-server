import datetime
import os

from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from utils import functions
import forms.forms
from routes import api

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

app.register_blueprint(api.bp)
bootstrap = Bootstrap5(app)


@app.route('/')
def hello_world():  # put application's code here
	return render_template('index.html')


@app.route('/environments')
def environments():
	return render_template('environments.html', log_e=[{"e": "Matteo", "t": datetime.datetime.now()}],
	                       logs=[datetime.datetime.now(), datetime.datetime.now()])


@app.route('/devices')
def devices():
	form = forms.forms.addDevice()
	form.employee.choices = functions.employee_choices(api.session)
	return render_template('devices.html', devices=functions.getDevices(api.session), new_device=form)


@app.route('/employees')
def employees():
	return render_template('employees.html', employees=functions.getEmployees(api.session))


@app.route('/devices/<int:device_id>')
def edit_device(device_id):
	form = functions.getDeviceForm(api.session, device_id)
	return render_template('edit_device.html', form=form)




@app.route('/logs')
def logs():
	return render_template('logs.html')


if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(debug=True, host='0.0.0.0', port=port)
