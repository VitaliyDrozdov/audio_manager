from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.dependencies import Base

if TYPE_CHECKING:
    from src.users.models import UserProfile


class AudioFile(Base):
    __tablename__ = "audio_files"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    filename: Mapped[str] = mapped_column(String(100), nullable=False)
    filepath: Mapped[str] = mapped_column(String(), nullable=False)
    description: Mapped[str] = mapped_column(String(), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(), nullable=False, default=datetime.now(timezone.utc)
    )
    updated_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(), nullable=True, onupdate=datetime.now(timezone.utc)
    )
    owner_id: Mapped[int] = mapped_column(ForeignKey("userprofile.id"))

    owner: Mapped["UserProfile"] = relationship(
        "UserProfile", back_populates="audio_files"
    )
