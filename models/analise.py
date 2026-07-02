from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime
from database.connection import Base

class AnaliseModel(Base):
    __tablename__ = "analises"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    image_path = Column(String(500), nullable=False)
    descricao = Column(String(1000), nullable=True)
    objetos = Column(String(1000), nullable=True)
    quantidade_pessoas = Column(Integer, default=0)
    rostos = Column(Integer, default=0)
    idade = Column(String(100), nullable=True)
    emocao = Column(String(100), nullable=True)
    cores = Column(String(255), nullable=True)
    luminosidade = Column(String(100), nullable=True)
    nitidez = Column(String(100), nullable=True)
    transcricao = Column(String(2000), nullable=True)
    json_resultado = Column(JSON, nullable=True)
