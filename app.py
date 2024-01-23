import os

from flask import Flask, render_template, request, Response
from flask_bootstrap import Bootstrap5
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import forms.forms
from routes import api
from utils import functions

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

app.register_blueprint(api.bp)
bootstrap = Bootstrap5(app)


@app.route('/', methods=['GET', 'POST'])
def home():  # put application's code here
	if request.method == 'POST':
		msg = request.get_json()
		api.chat_id = msg["message"]["chat"]["id"]
		return Response('ok', status=200)
	total_employees, total_customers = functions.get_total_count(api.session)
	return render_template('index.html', total_employees=total_employees, total_customers=total_customers)


@app.route('/environments')
def environments():
	logs, employee_logs = functions.get_logs(api.session)
	security = functions.get_security_level(api.session)
	return render_template('environments.html', security=security, employee_logs=employee_logs, logs=logs)


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
	app.run(debug=True, port=port)
