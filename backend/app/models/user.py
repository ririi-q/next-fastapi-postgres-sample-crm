from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base_class import BaseWithTimestamps

# table of user_company many-to-many relationship
user_company = Table('user_company', BaseWithTimestamps.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('company_id', Integer, ForeignKey('companies.id'))
)

class User(BaseWithTimestamps):
    __tablename__ = 'users'

    # Attributes
    id = Column(Integer, primary_key=True, index=True) # ID
    name = Column(String, index=True) # 名前
    email = Column(String, unique=True, index=True) # メールアドレス
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    # Relationships of Company many-to-many
    companies = relationship("Company", secondary=user_company, back_populates="users")

    # Constraints
    __table_args__ = (UniqueConstraint('email', name='uq_user_email'),) # DBレベルでのユニーク制約

    def __str__(self):
        return f"User(id={self.id}, name={self.name}, email={self.email})"
