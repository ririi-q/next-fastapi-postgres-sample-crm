from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base_class import BaseWithTimestamps
from app.models.user import user_company  # 中間テーブル


class Company(BaseWithTimestamps):
    __tablename__ = 'companies'

    # Attributes
    id = Column(Integer, primary_key=True, index=True) # ID
    name = Column(String, index=True) # 名前
    domain = Column(String, unique=True, index=True, nullable=False)  # ドメイン

    # Relationships of User many-to-many
    users = relationship("User", secondary=user_company, back_populates="companies")

    # Constraints
    __table_args__ = (UniqueConstraint('domain', name='uq_company_domain'),) # DBレベルでのユニーク制約

    def __str__(self):
        return f"Company(id={self.id}, name={self.name}, domain={self.domain})"
