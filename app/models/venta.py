from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base

class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, index=True)
    cliente = Column(String, index=True)
    producto = Column(String)
    monto = Column(Float)
    estado = Column(String)
    color = Column(String)
