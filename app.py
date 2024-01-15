import os

from flask import Flask, render_template
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from User import Users,Kind

db_name = 'nenno'
db_user = 'username'
db_pass = 'cacca'
db_host = 'db'
db_port = '5432'
db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
db = create_engine(db_string)
session = Session(bind=db)
app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    u = Users(id=2, name="Matteo", surname="nenno", kind=Kind.normal, device_id=2, last_location=None, last_read=None)
    session.add(u)
    session.commit()
    with db.connect() as conn:
        result = conn.execute(
            text('SELECT * FROM "Users"'))
    return render_template('index.html', result=result.all())


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
