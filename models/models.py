import datetime
import enum
from typing import List

from sqlalchemy import Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, QueryableAttribute


class Base(DeclarativeBase):
	pass


class Kind(enum.Enum):
	"""
	Enum used to define the kind of user
	"""
	normal = "normal"
	privileged = "privileged"


class User(Base):
	"""
	Model used to describe a user
	"""
	__tablename__ = 'Users'
	id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
	name: Mapped[str] = mapped_column(String(50), nullable=False)
	surname: Mapped[str] = mapped_column(String(50), nullable=False)
	kind: Mapped[Kind]
	device_id: Mapped[int] = mapped_column(ForeignKey("Devices.id"), nullable=False)
	last_location: Mapped[int] = mapped_column(Integer)
	last_read: Mapped[datetime.datetime] = mapped_column(TIMESTAMP)
	logs: Mapped[List["Log"]] = relationship(back_populates='u')


class Device(Base):
	__tablename__ = 'Devices'
	id: Mapped[int] = mapped_column(Integer, primary_key=True)
	mac_address: Mapped[str] = mapped_column(String(17), unique=True, nullable=False)
	enabled: Mapped[bool] = mapped_column(Boolean, default=False)


class Room(Base):
	__tablename__ = 'Rooms'
	id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
	name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
	kind: Mapped[Kind]


class Log(Base):
	__tablename__ = 'Logs'
	id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
	timestamp: Mapped[datetime.datetime] = mapped_column(TIMESTAMP, nullable=False)
	action: Mapped[int] = mapped_column(Integer, nullable=False)
	room: Mapped[int] = mapped_column(ForeignKey("Rooms.id"), nullable=False)
	user: Mapped[int] = mapped_column(ForeignKey("Users.id"), nullable=True)
	u: Mapped["User"] = relationship(back_populates="logs")
