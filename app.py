import os

from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from routes import api
app = Flask(__name__)
app.register_blueprint(api.bp)
bootstrap = Bootstrap5(app)


@app.route('/')
def hello_world():  # put application's code here
	return render_template('index.html')


if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(debug=True, host='0.0.0.0', port=port)
