import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, TIMESTAMP, Enum
import sqlalchemy.types as types
import enum


class Base(DeclarativeBase):
	pass


class Kind(enum.Enum):
	normal = "normal"
	privileged = "privileged"


class Users(Base):
	__tablename__ = 'Users'
	id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
	name: Mapped[str] = mapped_column(String(50), nullable=False)
	surname: Mapped[str] = mapped_column(String(50), nullable=False)
	kind: Mapped[Kind]
	device_id: Mapped[int] = mapped_column(Integer)
	last_location: Mapped[int] = mapped_column(Integer)
	last_read: Mapped[datetime.datetime] = mapped_column(TIMESTAMP)
