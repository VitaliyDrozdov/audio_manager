import enum
from typing import TYPE_CHECKING, List

from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.db_accessor import Base

if TYPE_CHECKING:
    from src.audio.models import AudioFile


class Roles(enum.Enum):
    SIMPLE_USER = 0
    ADMIN = 1
    SUPERUSER = 2


class UserProfile(Base):
    __tablename__ = "userprofile"
    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    username: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True
    )
    password_hash: Mapped[str] = mapped_column(String(100), nullable=False)
    first_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    role: Mapped[int] = mapped_column(
        Enum(Roles, native_enum=True),
        nullable=False,
        default=Roles.SIMPLE_USER,
    )
    audio_files: Mapped[List["AudioFile"]] = relationship(
        "AudioFile",
        back_populates="owner",
        uselist=True,
        single_parent=True,
        cascade="all, delete-orphan",
    )
