import datetime

import sqlalchemy.exc
from werkzeug.datastructures import MultiDict
import forms.forms
from models.models import Log, User, Device, Room, Kind
from telegram import Update
from telegram.ext import ApplicationBuilder,CommandHandler,ContextTypes

def add_log(session, event, room, user=None):
	l = Log(timestamp=datetime.datetime.now(), action=event, room=room, user=user)
	session.add(l)
	session.commit()


def employee_choices(session):
	employees = session.query(User).where(User.device_id == None).all()
	print(employees)
	choices = []
	for e in employees:
		choices.append((e.id, e.name + " " + str(e.surname)))
	choices.append((-1, "None"))
	return choices


def getDevices(session):
	devices = session.query(Device).order_by(Device.id).all()

	render_devices = []
	for d in devices:
		try:
			employee = session.query(User).where(User.device_id == d.id).one()
			employee = employee.name + " " + employee.surname
		except sqlalchemy.exc.NoResultFound:
			employee = None

		render_device = {
			"id": d.id,
			"mac_address": d.mac_address,
			"employee": employee,
			"enabled": d.enabled
		}
		render_devices.append(render_device)
	return render_devices


def getDeviceForm(session, device_id):
	device = session.query(Device).where(Device.id == device_id).one()
	try:
		employee = session.query(User).where(User.device_id == device_id).one()
		employee_id = employee.id
	except sqlalchemy.exc.NoResultFound:
		employee_id = -1

	formData = {
		"mac_address": device.mac_address,
		"employee": employee_id,
		"device_id": device_id}
	if device.enabled:
		formData["enabled"] = "y"
	form = forms.forms.addDevice(
		formdata=MultiDict(formData))
	form.employee.choices = employee_choices(session)
	if employee_id != -1:
		form.employee.choices.append((employee.id, employee.name + " " + employee.surname))
	return form


def getEmployees(session):
	employees = session.query(User).order_by(User.id).all()
	render_employees = []
	for e in employees:
		current_level = "Normal" if e.kind == Kind.normal else "Privileged"
		form = forms.forms.permissionForm()
		form.permission.data = current_level.lower()
		render_employee = {
			"employee_id": str(e.id),
			"name": e.name + " " + e.surname,
			"kind": form
		}
		if e.last_read is not None and e.last_location is not None:
			render_employee["time"] = e.last_read
			room = session.query(Room).where(Room.id == e.last_location).first()
			render_employee["room"] = room.name
		else:
			render_employee["time"] = None
			render_employee["room"] = None
		render_employees.append(render_employee)
	return render_employees


def get_logs(session):
	rooms = [(room.name, room.id, room.num_employees, room.num_customers) for room in session.query(Room).all()]
	logs = {}
	employee_logs = {}
	for room in rooms:
		_, room_id, num_employees, num_customers = room
		logs[room_id] = {"data": session.query(Log).where(Log.room == room_id).filter(Log.user == None).all()}
		logs[room_id]["len"] = num_customers
		employee_logs[room_id] = {
			"data": session.query(Log, User).where(Log.room == room_id).filter(Log.user != None).filter(
				Log.user == User.id).all()}
		employee_logs[room_id]["len"] = num_employees
	return logs, employee_logs


def get_security_level(session):
	rooms = session.query(Room).order_by(Room.id).all()
	rooms = [(room.id, "Normal" if room.kind == Kind.normal else "Privileged") for room in rooms]
	return rooms


def get_total_count(session):
	rooms = session.query(Room).order_by(Room.id).all()
	total_customers = 0
	total_employees = 0
	for room in rooms:
		total_customers += room.num_customers
		total_employees += room.num_employees
	return total_employees, total_customers

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
	await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
