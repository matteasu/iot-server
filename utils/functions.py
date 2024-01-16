import datetime

from models.models import Log


def add_log(session, event, room, user=None):
	l = Log(timestamp=datetime.datetime.now(), action=event, room=room, user=user)
	session.add(l)
	session.commit()
