import os

from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from werkzeug.datastructures import MultiDict
import forms.devices
from routes import api

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# app.register_blueprint(api.bp)
bootstrap = Bootstrap5(app)


@app.route('/')
def hello_world():  # put application's code here
	return render_template('index.html')


@app.route('/environments')
def environments():
	return render_template('environments.html')


@app.route('/devices')
def devices():
	devices = [("0", "AAAA"), ("1", "nenno")]
	form = forms.devices.addDevice(formdata=MultiDict({"mac_address": "ciao", "employee": "1", "enabled": "True"}))
	form.employee.choices = devices
	return render_template('devices.html', form=form)


if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(debug=True, host='0.0.0.0', port=port)
