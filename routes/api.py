from flask import request, Blueprint
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models.models import User, Device, Room
import json
import datetime

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
		return "user auth"
	else:
		return "{} is not authorized to enter {}".format(user.name, room.name)
