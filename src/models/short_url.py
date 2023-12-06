from datetime import datetime

from sqlalchemy import String, Text, DateTime, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class ShortUrl(DeclarativeBase):
    __tablename__ = "short_url"

    short_id: Mapped[str] = mapped_column(String(10), primary_key=True)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("current_timestamp()")
    )
