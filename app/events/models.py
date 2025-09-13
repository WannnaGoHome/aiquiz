import enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum, ForeignKey, Column, Table, Integer

from app.common.db import Base

class EventStatus(str, enum.Enum):
    NOT_STARTED = "not_started"
    REGISTRATION = "registration"
    STARTED = "started"
    FINISHED = "finished"

event_players = Table(
    "event_players",
    Base.metadata,
    Column("event_id", ForeignKey("events.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)

class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    status: Mapped[EventStatus] = mapped_column(Enum(EventStatus, name="game_status"), default=EventStatus.NOT_STARTED, nullable=False)
    current_question_index: Mapped[int] = mapped_column(default=0, nullable=False)

    # создатель ивента (один User -> много Event)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    creator: Mapped["User"] = relationship(back_populates="created_events", lazy="selectin")

    # вопросы (один Event -> много Questions)
    questions: Mapped[list["Question"]] = relationship(back_populates="event")

    # игроки (many-to-many)
    players: Mapped[list["User"]] = relationship(
    secondary="event_players",
    back_populates="events",
    lazy="selectin"
)


class Question(Base):
    __tablename__ = "questions" 

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(String(255), nullable=False)

    # привязка к ивенту
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False)
    event: Mapped["Event"] = relationship(back_populates="questions", lazy="selectin")
    