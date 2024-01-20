import datetime

import sqlalchemy.exc
from werkzeug.datastructures import MultiDict
import forms.devices
from models.models import Log, User, Device


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
	return choices


def getDevices(session):
	devices = session.query(Device).all()

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
	employee = session.query(User).where(User.device_id == device_id).one()
	form = forms.devices.addDevice(
		formdata=MultiDict({"mac_address": device.mac_address, "employee": employee.id, "enabled": device.enabled}))
	form.employee.choices = employee_choices(session)

	form.employee.choices.append((employee.id, employee.name + " " + employee.surname))
	return form
