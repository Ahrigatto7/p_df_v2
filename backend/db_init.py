import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from backend.models import Base
from backend.db import engine

Base.metadata.create_all(bind=engine)
print("✅ DB 초기화 완료")