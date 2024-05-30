# Importa os esquemas de dados para Calouros e Voluntarios.
from app.schema.schema import DadosSchema_Calouros, DadosSchema_Voluntarios

# Importa os modelos de banco de dados para Calouros e Voluntarios.
from app.models.models import Calouros, Voluntarios

# Remove acentos de strings.
from unidecode import unidecode

def consulta_geral_Calouros() -> list:
    """
    Consulta todos os registros de calouros no banco de dados.

    Returns:
        list: Uma lista contendo todos os registros de calouros.
    """
    # Realiza a consulta no banco de dados para buscar todos os registros de calouros.
    consulta = Calouros.query.all()
    return consulta

def consulta_frequencia_Calouros(Nome: str, email: str, dia: str) -> bool:
    """
    Verifica se existe um registro de frequência para um calouro em um determinado dia.

    Args:
        Nome (str): O nome do calouro.
        email (str): O email do calouro.
        dia (str): A data para a qual a frequência está sendo verificada.

    Returns:
        bool: True se houver um registro de frequência para o calouro na data especificada, False caso contrário.
    """
    # Realiza a consulta no banco de dados para buscar o registro de frequência do calouro no dia especificado.
    consulta = Calouros.query.filter_by(
        nome=unidecode(Nome),  # Remove acentos do nome.
        email=email,
        data=dia
    ).all()
    
    # Serializa os dados da consulta usando o esquema de dados para Calouros.
    dados = DadosSchema_Calouros(many=True).dumps(consulta, indent=2)
    print(dados)
    print(dia)
    
    # Retorna True se houver um registro de frequência para o calouro na data especificada.
    return dia in dados

def consulta_frequencia_Voluntarios(Nome: str, email: str, dia: str) -> bool:
    """
    Verifica se existe um registro de frequência para um voluntário em um determinado dia.

    Args:
        Nome (str): O nome do voluntário.
        email (str): O email do voluntário.
        dia (str): A data para a qual a frequência está sendo verificada.

    Returns:
        bool: True se houver um registro de frequência para o voluntário na data especificada, False caso contrário.
    """
    # Realiza a consulta no banco de dados para buscar o registro de frequência do voluntário no dia especificado.
    consulta = Voluntarios.query.filter_by(
        nome=unidecode(str(Nome).strip()),  # Remove acentos e espaços extras do nome.
        email=email,
        data=dia
    ).all()
    
    # Serializa os dados da consulta usando o esquema de dados para Voluntarios.
    dados = DadosSchema_Voluntarios(many=True).dumps(consulta, indent=2)
    print(dados)
    print(dia)
    
    # Retorna True se houver um registro de frequência para o voluntário na data especificada.
    return dia in dados

def dicionario_resposta(Nome: str, email: str) -> dict:
    """
    Cria um dicionário de resposta para o caso em que não é necessário adicionar um novo registro.

    Args:
        Nome (str): O nome do aluno ou voluntário.
        email (str): O email do aluno ou voluntário.

    Returns:
        dict: Um dicionário contendo o nome do aluno ou voluntário, email e a contagem de registros associados ao email.
    """
    # Retorna um dicionário com os dados do aluno ou voluntário e a contagem de registros para o email.
    return {'student-name': Nome, 'email': email, 'count': int(Calouros.query.filter_by(email=email).count())}
