from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# 以下の行を追加して、すべてのモデルをインポートします
from app.models.user import User
# 他のモデルがある場合は、ここに追加してください
