from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    categoria = Column(String, index=True)
    icon = Column(String)
    titulo = Column(String)
    valor = Column(String)
    color = Column(String)
