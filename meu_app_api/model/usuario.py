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
    cep = Column(String(9), unique=False)
    logradouro = Column(String(256), unique=False)
    bairro = Column(String(256), unique=False)
    cidade = Column(String(256), unique=False)
    estado = Column(String(2), unique=False)
    
    # Definição do relacionamento entre o usuario e o histórico.
    # Essa relação é implicita, não está salva na tabela 'usuario',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    historicos = relationship("Historico", back_populates="usuario_obj")


    def __init__(self, nome: str, email: str, senha: str, cep: str, logradouro: str, bairro: str, cidade: str, estado: str):
        """
        Cria um registro de usuario

        Arguments:
            nome: nome do usuário
            email: e-mail do usuário
            senha: senha do usuário
            cep: CEP do usuário
            logradouro: logradouro do usuário
            bairro: bairro do usuário
            cidade: cidade do usuário
            estado: estado do usuário
        """
        self.nome = nome
        self.email = email
        self.senha = senha
        self.cep = cep
        self.logradouro = logradouro
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado

    def adiciona_historico(self, historico:Historico):
        """ Adiciona um novo histórico ao registro de usuario.
        """
        self.historicos.append(historico)

