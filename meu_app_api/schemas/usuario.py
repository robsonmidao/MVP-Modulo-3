from pydantic import BaseModel
from typing import Optional, List
from model.usuario import Usuario

from schemas import HistoricoSchema
from schemas.historico import CategoriaBuscaHistoricoSchema


class UsuarioSchema(BaseModel):
    """ Define como um novo registro de usuário a ser inserido deve ser representado
    """
    nome: str 
    email: str
    senha: str 
    cep: str
    logradouro: str
    bairro: str
    cidade: str
    estado: str
   

class UsuarioBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do registro de usuário.
    """
    nome: str 

class UsuarioBuscaLoginSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do registro de usuário.
    """
    email: str 
    senha: str 
        
class UsuarioBuscaHistoricoSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do registro de usuário.
    """
    nome: str
    
class UsuarioBuscaExclusaoSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id do registro de usuário.
    """
    id: int 
    
class UsuarioSchemaUpdate(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id do registro de usuário.
    """
    id: int 
    nome: str 
    cep: str
    cidade: str
    estado: str
    logradouro:str
    bairro: str
        
class ListagemUsuarioSchema(BaseModel):
    """ Define como uma listagem de registro de usuário será retornada.
    """
    usuarios:List[UsuarioSchema]


def apresenta_usuarios(usuarios: List[Usuario]):
    """ Retorna uma representação do registro de usuário seguindo o schema definido em
        UsuarioViewSchema.
    """
    result = []
    for usuario in usuarios:
        result.append({
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "senha": usuario.senha,
            "cep": usuario.cep,
            "logradouro": usuario.logradouro,
            "bairro": usuario.bairro,
            "cidade": usuario.cidade,
            "estado": usuario.estado            
        })

    return {"usuarios": result}


class UsuarioViewSchema(BaseModel):
    """ Define como um usuário será retornado: usuário + histórico.
    """
    id: int 
    nome: str 
    email: str 
    senha: str 
    cep: str
    logradouro: str
    bairro: str
    cidade: str
    estado: str
    historicos: List[UsuarioSchema]

class HistoricoViewSchema(BaseModel):
    """ Define como um usuário será retornado: usuário + histórico.
    """
    id: int 
    categoria: str 
    score: str 
    data: str
    nome: str 


class UsuarioDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    id: int
   

def apresenta_usuario(usuario: Usuario):
    """ Retorna uma representação do registro de usuário seguindo o schema definido em
        UsuarioViewSchema.
    """
    return {    
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "senha": usuario.senha,
        "cep": usuario.cep,
        "logradouro": usuario.logradouro,
        "bairro": usuario.bairro,
        "cidade": usuario.cidade,
        "estado": usuario.estado,
        "historicos": [{"categoria": c.categoria, "score": c.score, "data": c.data_insercao} for c in usuario.historicos]
    }


def apresenta_login(usuario: Usuario):
    """ Retorna uma representação do registro de usuário seguindo o schema definido em
        UsuarioViewSchema.
    """
    return {    
        "nome": usuario.nome,
        "id": usuario.id
    }