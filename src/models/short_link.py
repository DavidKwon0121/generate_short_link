from datetime import datetime

from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from src.modules.database import Base


class ShortLink(Base):
    __tablename__ = "short_link"
    __table_args__ = {"extend_existing": True}

    short_id: Mapped[str] = mapped_column(String(6), primary_key=True)
    url_str: Mapped[str] = mapped_column(Text, nullable=False)
    url_hash: Mapped[str] = mapped_column(
        String(32), nullable=False, unique=True, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow()
    )

    def return_camelize(self) -> dict:
        return dict(
            data=dict(
                shortId=self.short_id,
                url=self.url_str,
                createdAt=self.created_at.isoformat(),
            )
        )
