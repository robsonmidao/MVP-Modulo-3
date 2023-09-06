from pydantic import BaseModel
from typing import List
from model.historico import Historico

class HistoricoSchema(BaseModel):
    """ Define como um novo histórico a ser inserido deve ser representado
    """
    usuario_id: int 
    categoria: str
    score: str 
    data: str 
    
class CategoriaSchema(BaseModel):
    """ Define como um novo registro de categoria a ser inserido deve ser representado
    """
    nome: str 
    score: str
    data: str

class CategoriaBuscaHistoricoSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base na categoria do registro de histórico.
    """
    categoria: str
    
def apresenta_historico(historico: Historico):
    """ Retorna uma representação do registro de histórico seguindo o schema definido.
    """
    return {
        "id": historico.id,
        "categoria": historico.categoria,
        "score": historico.score,
        "data": historico.data_insercao,
        "nome": historico.usuario_obj.nome  
    }


def apresenta_historicos(historicos: List[Historico]):
    return [apresenta_historico(historico) for historico in historicos]
