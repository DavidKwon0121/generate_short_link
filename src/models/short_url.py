from datetime import datetime

from sqlalchemy import String, Text, DateTime, FetchedValue
from sqlalchemy.orm import Mapped, mapped_column

from src.modules.database import Base


class ShortUrl(Base):
    __tablename__ = "short_url"

    short_id: Mapped[str] = mapped_column(String(6), primary_key=True)
    url_str: Mapped[str] = mapped_column(Text, nullable=False)
    url_hash: Mapped[str] = mapped_column(String(32), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=FetchedValue()
    )

    def return_camelize(self) -> dict:
        return dict(
            data=dict(
                shortId=self.short_id,
                url=self.url_str,
                createdAt=self.created_at.isoformat(),
            )
        )
