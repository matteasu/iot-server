from flask import request, Blueprint, render_template, redirect
from sqlalchemy import create_engine
import sqlalchemy.exc
from sqlalchemy.orm import Session
from models.models import User, Device, Room, Log, Kind
from utils import functions

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
		return "Ok", 200
	else:
		return "Not ok", 404


@bp.route('/getLogs', methods=['GET'])
def get_logs():
	logs = session.query(Log).all()
	render_logs = []
	for log in logs:
		if log.user is None:
			user = "customer"
		else:
			q = session.query(User.name, User.surname).where(User.id == log.user).one()
			user = q.name + " " + q.surname
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


@bp.route('/addDevice', methods=['POST'])
def save_device():
	if request.form is not None:
		data = request.form
	enabled = data.get('enabled', default=False)
	if enabled == "y":
		enabled = True
	d = Device(mac_address=data['mac_address'], enabled=enabled)
	session.add(d)
	if data["employee"] != "-1":
		employee = session.query(User).where(User.id == data['employee']).one()
		employee.device_id = d.id
		session.add(employee)
	session.commit()
	return redirect('/devices')


@bp.route('/editDevice', methods=['POST'])
def edit_device():
	if request.form is not None:
		data = request.form
	try:
		old_employee = session.query(User).where(User.device_id == data["device_id"]).one()
	except sqlalchemy.orm.exc.NoResultFound:
		old_employee = None
	device = session.query(Device).where(Device.id == data["device_id"]).one()
	enabled = data.get('enabled', default=False)
	if enabled == "y":
		enabled = True
	device.enabled = enabled
	device.mac_address = data['mac_address']
	if old_employee is not None:
		if data['employee'] != old_employee.id:
			old_employee.device_id = None
			session.add(old_employee)
	employee = session.query(User).where(User.id == data['employee']).one()
	employee.device_id = data['device_id']
	session.add(employee)
	session.add(device)
	session.commit()
	return redirect('/devices')


@bp.route('/edit_employees/<int:employee_id>', methods=['POST'])
def edit_permissions(employee_id):
	if request.form is not None:
		data = request.form
		u = session.query(User).where(User.id == employee_id).one()
		if data['permission'] == "normal":
			u.kind = Kind.normal
		elif data['permission'] == "privileged":
			u.kind = Kind.privileged
		session.add(u)
		session.commit()
		return redirect("/employees")
