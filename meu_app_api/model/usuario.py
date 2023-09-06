from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Historico


class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True)
    nome = Column(String(140), unique=False)
    email = Column(String(256), unique=False)
    senha = Column(String(256), unique=False)
    
    # Definição do relacionamento entre o usuario e o histórico.
    # Essa relação é implicita, não está salva na tabela 'usuario',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    historicos = relationship("Historico", back_populates="usuario_obj")


    def __init__(self, nome:str, email:str, senha:str):
        """
        Cria um registro de usuario

        Arguments:
            nome: nome do usuário
            email: e-mail do usuário
            senha: senha do usuário
        """
        self.nome = nome
        self.email = email
        self.senha = senha

    def adiciona_historico(self, historico:Historico):
        """ Adiciona um novo histórico ao registro de usuario.
        """
        self.historicos.append(historico)

