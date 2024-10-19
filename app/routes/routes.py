# Importa componentes do micro framework Flask que serve para criar aplicações web
from flask import jsonify, send_file, redirect, url_for

# Indica retorno de múltiplos tipos de dados.
from typing import Union, List

# Importa as funções da views
from app.views.views import index, Registro_Frequencia, consulta_presenca, download_Arquivo

from . import bp

@bp.route('/')
@bp.route('/home')
def home() -> str:
    """
    Renderiza a página inicial.

    Returns:
        str: O conteúdo renderizado do template index.html.
    """
    return index()

@bp.route("/Frequencia", methods=['GET', 'POST'])
def frequencia() -> jsonify:
    """
    Registra a frequência dos alunos ou voluntários.

    Returns:
        jsonify: Um JSON contendo os dados registrados e o número total de registros para o email correspondente.
    """
    return Registro_Frequencia()

@bp.errorhandler(404)
def page_not_found(e):
    """
    Redireciona para a página inicial em caso de erro 404.

    Args:
        e: Exceção gerada pelo erro 404.

    Returns:
        redirect: Redireciona o usuário para a página inicial.
    """
    return redirect(url_for('home'))

@bp.route("/consulta", methods=['GET', 'POST'])
@bp.route("/consulta/entidade=<entidade>", methods=['GET', 'POST'])
@bp.route("/consulta/nome=<nome>&entidade=<entidade>", methods=['GET', 'POST'])
def consulta(entidade: str = None, nome: str = None) -> Union[str, List[List[Union[int, str]]]]:
    """
    Consulta os registros de frequência.

    Args:
        entidade (str, optional): A entidade para a qual a consulta de presença será realizada.
        nome (str, optional): O nome para o qual a consulta de presença será realizada.

    Returns:
        Union[str, List[List[Union[int, str]]]]: O resultado da consulta, que pode ser uma string ou uma lista de listas contendo inteiros ou strings.
    """
    return consulta_presenca(entidade, nome)

@bp.route('/download', methods=['GET'])
def download() -> Union[send_file, redirect]:
    """
    Baixa o arquivo de frequência.

    Returns:
        Union[send_file, redirect]: O arquivo a ser baixado ou um redirecionamento.
    """
    return download_Arquivo()
