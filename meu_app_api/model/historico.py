from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union
from sqlalchemy.orm import relationship

from  model import Base


class Historico(Base):
    __tablename__ = 'historico'

    id = Column(Integer, primary_key=True)
    categoria = Column(String(256))
    score = Column(String(32))
    data_insercao = Column(DateTime, default=datetime.now())
    
    # Definição do relacionamento entre o histórico e um usuário.
    # Aqui está sendo definido a coluna 'usuário' que vai guardar
    # a referencia ao usuário, a chave estrangeira que relaciona
    # um usuário ao histórico.
    usuario = Column(Integer, ForeignKey("usuario.id"), nullable=False)

    # ... também armazene uma referência ao objeto Usuario associado:
    usuario_obj = relationship("Usuario", back_populates="historicos")


    def __init__(self, idUsuario:str, categoria:str, score:str, data_insercao:Union[DateTime, None] = None):
        """
        Cria um Histórico

        Arguments:           
            categoria: Categoria do quiz.
            score: quantidade de acertos / total de acertos no quiz.
            data_insercao: data de quando o registro foi feito ou inserido
                           à base
        """        
        self.categoria = categoria
        self.score = score
        if data_insercao:
            self.data = data_insercao
