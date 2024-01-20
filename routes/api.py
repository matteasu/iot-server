from flask import request, Blueprint, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models.models import User, Device, Room, Log
from utils import functions
from fastapi.encoders import jsonable_encoder

db_name = 'nenno'
db_user = 'username'
db_pass = 'cacca'
db_host = 'db'
db_port = '5432'
db_string = 'postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name)
db = create_engine(db_string)
session = Session(bind=db)
bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/openDoor', methods=['POST'])
def open_door():
	if request.json is not None:
		parsed = request.get_json()
	else:
		return "error"
	device = session.query(Device).where(Device.mac_address == parsed["device"]).one()
	device = device.id
	user = session.query(User).where(User.device_id == device).one()
	room = session.query(Room).where(Room.id == parsed["room"]).one()
	if room.kind == user.kind:
		functions.add_log(session, 0, room.id, user.id)
		return "user auth"
	else:
		return "{} is not authorized to enter {}".format(user.name, room.name)


@bp.route('/getLogs', methods=['GET'])
def get_logs():
	logs = session.query(Log).all()
	render_logs = []
	for log in logs:
		if log.user is None:
			user = "customer"
		else:
			q = session.query(User.name, User.surname).where(User.id == log.user).one()
			user = q.name + " "+q.surname
		q = session.query(Room).where(Room.id == log.room).one()
		room = q.name
		render_log = {
			"user": user,
			"time": log.timestamp,
			"room": room,
			"action": "enter" if log.action == 0 else "leave"
		}
		render_logs.append(render_log)
	return render_template("components/log_table.html", logs=render_logs)
