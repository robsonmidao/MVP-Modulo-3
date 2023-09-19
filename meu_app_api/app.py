from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Usuario, Historico
from logger import logger
from schemas import *
from flask_cors import CORS
from schemas.historico import CategoriaBuscaHistoricoSchema, apresenta_historico, apresenta_historicos

from schemas.usuario import HistoricoViewSchema, UsuarioBuscaHistoricoSchema, UsuarioBuscaLoginSchema, UsuarioSchemaUpdate, apresenta_login 

info = Info(title="Controle de Usuario", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
usuario_tag = Tag(name="Usuario", description="Adição, visualização e remoção de registros de usuario à base")
historico_tag = Tag(name="Historico", description="Adição de um histórico à um registro de usuario cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/usuario', tags=[usuario_tag],
          responses={"200": UsuarioViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_usuario():
    """Adiciona um novo registro de usuario à base de dados

    Retorna uma representação dos registros de usuario e históricos associados.
    """
    data = request.json
    usuario = Usuario(
        nome=data['nome'],
        email=data['email'],
        senha=data['senha'],
        cep=data['cep'],
        logradouro=data['logradouro'],
        bairro=data['bairro'],
        cidade=data['cidade'],
        estado=data['estado']
    )
    try:
        # criando conexão com a base
        session = Session()
        # adicionando registro de usuario
        session.add(usuario)
        # efetivando o camando de adição de novo item na tabela
        session.commit()  
        return {"message": "Usuário adicionado com sucesso!", "usuario": apresenta_usuario(usuario)}, 200


    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Registro de usuário de mesmo email já salvo na base :/"
        logger.warning(f"Erro ao adicionar registro de usuário '{usuario.email}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        logger.error(f"Erro ao adicionar registro de usuario: {e}")
        return {"mesage": "Ocorreu um erro ao adicionar o usuário."}, 400



@app.get('/usuarios', tags=[usuario_tag],
         responses={"200": ListagemUsuarioSchema, "404": ErrorSchema})
def get_usuarios():
    """Faz a busca por todos os registros de usuario cadastrados

    Retorna uma representação da listagem de registros de usuario.
    """
    logger.debug(f"Coletando registros de usuario ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    usuarios = session.query(Usuario).all()

    if not usuarios:
        # se não há usuarios cadastrados
        return {"usuários": []}, 200
    else:
        logger.debug(f"%d usuários econtrados" % len(usuarios))
        # retorna a representação de registro de usuario
        print(usuarios)
        return apresenta_usuarios(usuarios), 200


@app.get('/usuario', tags=[usuario_tag],
         responses={"200": UsuarioViewSchema, "404": ErrorSchema})
def get_usuario(query: UsuarioBuscaSchema):
    """Faz a busca por um registro de usuario a partir do nome do usuario

    Retorna uma representação dos registros de usuario e históricos associados.
    """
    usuario_nome = query.nome
    logger.debug(f"Coletando dados sobre usuario #{usuario_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a buscaPrata
    usuario = session.query(Usuario).filter(Usuario.nome == usuario_nome).first()

    if not usuario:
        # se o registro de usuario não foi encontrado
        error_msg = "Registro de usuario não encontrado na base :/"
        logger.warning(f"Erro ao buscar usuário '{usuario_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Registro de usuário econtrado: '{usuario.nome}'")
        # retorna a representação de registro de usuario
        return apresenta_usuario(usuario), 200
    

@app.post('/login', tags=[usuario_tag],
         responses={"200": UsuarioViewSchema, "403": ErrorSchema, "404": ErrorSchema})
def get_login():
    """Faz a busca por um registro de usuario a partir do email do usuario

    Retorna uma representação dos registros de usuario e históricos associados.
    """
    data = request.json
    usuario_email = data['email']
    usuario_senha = data['senha']
    
    logger.debug(f"Coletando dados sobre usuario #{usuario_email}")
    # criando conexão com a base
    session = Session()
    # fazendo a buscaPrata
    usuario = session.query(Usuario).filter(Usuario.email == usuario_email).first()

    if not usuario:
        # se o registro de usuario não foi encontrado
        error_msg = "Registro de usuario não encontrado na base :/"
        logger.warning(f"Erro ao buscar usuário '{usuario_email}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Registro de usuário econtrado: '{usuario.nome}'")
        if usuario.senha == usuario_senha:
            # retorna a representação de registro de usuario
            return apresenta_login(usuario), 200
        else:
            error_msg = "Senha incorreta para este usuário :/"
            return {"mesage": error_msg}, 403


@app.delete('/usuario', tags=[usuario_tag],
            responses={"200": UsuarioDelSchema, "404": ErrorSchema})
def del_usuario():
    """Deleta um registro de usuario a partir do id de usuario informado

    Retorna uma mensagem de confirmação da remoção.
    """
    data = request.json
    usuario_id = data['id']

    logger.debug(f"Deletando dados sobre registros de usuario #{usuario_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Usuario).filter(Usuario.id == usuario_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado registros de usuario #{usuario_id}")
        return {"mesage": "Registro de usuario removido", "id": usuario_id}
    else:
        # se o registro de usuario não foi encontrado
        error_msg = "Registro de usuario não encontrado na base :/"
        logger.warning(f"Erro ao deletar registro de usuario #'{usuario_id}', {error_msg}")
        return {"mesage": error_msg}, 404

@app.put('/usuario', tags=[usuario_tag], responses={"200": UsuarioViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def update_usuario():
    """Atualiza os detalhes de um usuário baseado em seu ID."""
    # Dados enviados no pedido.
    data = request.json
    usuario_id = data['id']
    
    # Criando uma sessão para se comunicar com o banco de dados.
    session = Session()
    
    # Procurando o usuário pelo ID fornecido.
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()

    # Se o usuário não for encontrado, retorne um erro.
    if not usuario:
        error_msg = "Usuário não encontrado :/"
        logger.warning(f"Erro ao atualizar o usuário com ID '{usuario_id}', {error_msg}")
        return {"message": error_msg}, 404

    # Se o usuário for encontrado, atualize seus detalhes.
    campos_atualizaveis = ["nome", "cep", "cidade", "estado", "logradouro", "bairro"]
    for campo in campos_atualizaveis:
        if campo in data:
            setattr(usuario, campo, data[campo])
    
    try:
        session.commit()
        logger.debug(f"Detalhes do usuário com ID '{usuario_id}' atualizado com sucesso.")
        return apresenta_usuario(usuario), 200
    except Exception as e:
        error_msg = "Erro ao atualizar os detalhes do usuário."
        logger.error(f"Erro ao atualizar os detalhes do usuário com ID '{usuario_id}', {error_msg}")
        return {"message": str(e)}, 400



@app.post('/historico', tags=[historico_tag],
          responses={"200": UsuarioViewSchema, "404": ErrorSchema})
def add_historico():
    """Adiciona um novo histórico à um registro de usuario cadastrado na base identificado pelo id

    Retorna uma representação dos registros de usuario e históricos associados.
    """
    data = request.json
    usuario_id  = data['user']
    logger.debug(f"Adicionando históricos ao registro de usuario #{usuario_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo registro de usuario
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        # se registro de usuario não encontrado
        error_msg = "Registro de usuario não encontrado na base :/"
        logger.warning(f"Erro ao adicionar histórico ao registro de usuario '{usuario_id}', {error_msg}")
        return {"mesage": error_msg}, 404

    # criando o histórico    
    categoria = data['category']
    score = data['score']
    data = data['date']
    historico = Historico(usuario_id,categoria,score,data)

    # adicionando o histórico ao registro de usuario
    usuario.adiciona_historico(historico)
    session.commit()

    logger.debug(f"Adicionado histórico ao registro de usuario #{usuario_id}")

    # retorna a representação de registro de usuario
    return apresenta_usuario(usuario), 200



@app.post('/por-usuario', tags=[historico_tag],
         responses={"200": HistoricoViewSchema, "404": ErrorSchema})
def get_consultaPorUsuario():
    """Faz a busca por um registro de histórico a partir do usuário

    Retorna uma representação dos registros de usuario e históricos associados.
    """
    data = request.json
    usuario_nome  = data['userName']
    logger.debug(f"Coletando dados sobre usuario #{usuario_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a buscaPrata
    usuario = session.query(Usuario).filter(Usuario.nome == usuario_nome).first()

    if not usuario:
        # se o registro de usuario não foi encontrado
        error_msg = "Registro de usuario não encontrado na base :/"
        logger.warning(f"Erro ao buscar usuário '{usuario_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Registro de usuário econtrado: '{usuario.nome}'")
        # retorna a representação de registro de usuario
        return apresenta_usuario(usuario), 200
    
    
    
@app.post('/por-categoria', tags=[historico_tag],
          responses={"200": HistoricoViewSchema, "404": ErrorSchema})
def get_consultaPorCategoria():
     """Faz a busca por registros de histórico a partir da categoria
    
     Retorna uma representação dos registros de usuario e históricos associados.
     """
     data = request.json
     categoria = data['categoryName'] 
     logger.debug(f"Coletando dados sobre categoria #{categoria}")
     # criando conexão com a base
     session = Session()
     # fazendo a busca
     categorias = session.query(Historico).filter(Historico.categoria == categoria).all()

     if not categorias or len(categorias) == 0:
         # se o registro de categoria não foi encontrado
         error_msg = "Registros da categoria não encontrados na base :/"
         logger.warning(f"Erro ao buscar categoria '{categoria}', {error_msg}")
         return {"mesage": error_msg}, 404
     else:
         logger.debug(f"{len(categorias)} registros de categoria encontrados para: '{categoria}'")
         # retorna a representação de registros de categoria
         return {"historicos": apresenta_historicos(categorias)}, 200
