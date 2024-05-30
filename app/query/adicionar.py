# Importa os modelos e a instância do banco de dados.
from app.models import db, Calouros, Voluntarios

# Remove acentos de strings.
from unidecode import unidecode

# Importa a classe date para manipulação de datas.
from datetime import date

def add_Calouros(Nome: str, email: str) -> dict:
    """
    Adiciona um novo registro de calouro ao banco de dados.

    Args:
        Nome (str): O nome do calouro.
        email (str): O email do calouro.

    Returns:
        dict: Um dicionário contendo o nome do calouro, email e a contagem de registros associados ao email.
    """
    # Cria uma nova instância de Calouros com os dados fornecidos.
    calouro = Calouros(
        nome=unidecode(str(Nome).strip()),  # Remove acentos e espaços extras do nome.
        email=email,  # Atribui o email fornecido.
        data=date.today()  # Define a data atual como data de registro.
    )
    
    # Adiciona o novo calouro à sessão do banco de dados.
    db.session.add(calouro)
    # Confirma a transação para salvar o registro no banco de dados.
    db.session.commit()
    
    # Retorna um dicionário com os dados do calouro e a contagem de registros para o email.
    return {'student-name': Nome, 'email': email, 'count': int(Calouros.query.filter_by(email=email).count())}

def add_Volountarios(Nome: str, email: str) -> dict:
    """
    Adiciona um novo registro de voluntário ao banco de dados.

    Args:
        Nome (str): O nome do voluntário.
        email (str): O email do voluntário.

    Returns:
        dict: Um dicionário contendo o nome do voluntário, email e a contagem de registros associados ao email.
    """
    # Cria uma nova instância de Voluntarios com os dados fornecidos.
    voluntario = Voluntarios(
        nome=unidecode(str(Nome).strip()),  # Remove acentos e espaços extras do nome.
        email=email,  # Atribui o email fornecido.
        data=date.today()  # Define a data atual como data de registro.
    )
    
    # Adiciona o novo voluntário à sessão do banco de dados.
    db.session.add(voluntario)
    # Confirma a transação para salvar o registro no banco de dados.
    db.session.commit()
    
    # Retorna um dicionário com os dados do voluntário e a contagem de registros para o email.
    return {'student-name': Nome, 'email': email, 'count': int(Voluntarios.query.filter_by(email=email).count())}
