from infra.configs.base import Base
from sqlalchemy import Column, String


class Usuario_pf(Base):
    __tablename__ = 'usuario'

    id = Column(String, primary_key=True)
    nome = Column(String, nullable=False)
    data_nasc = Column(String, nullable=False)
    email = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
