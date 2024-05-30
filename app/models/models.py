# Importa a extensão SQLAlchemy para interagir com o banco de dados
from . import db

# Define a classe de modelo para os Calouros
class Calouros(db.Model):
    """
    Classe que representa os dados dos alunos ou calouros.

    Attributes:
        id (int): Identificador único do aluno.
        nome (str): Nome do aluno.
        email (str): Endereço de email do aluno.
        data (datetime.date): Data do registro de frequência do aluno.

    Methods:
        to_json_Calouros(): Converte os dados do aluno em um dicionário JSON.
    """
    # Define os atributos da tabela Calouros
    id = db.Column(db.Integer, primary_key=True)  # Identificador único do aluno
    nome = db.Column(db.String(100), nullable=False)  # Nome do aluno
    email = db.Column(db.String(100), nullable=False)  # Endereço de email do aluno
    data = db.Column(db.Date, nullable=False)  # Data do registro de frequência do aluno
    
    def to_json_Calouros(self) -> dict:
        """
        Converte os dados do aluno para um dicionário JSON.

        Returns:
            dict: Dicionário contendo os dados do aluno.
        """
        return {'id': self.id, 'name': self.nome, 'email': self.email, 'data': self.data}

# Define a classe de modelo para os Voluntarios
class Voluntarios(db.Model):
    """
    Classe que representa os dados dos voluntários.

    Attributes:
        id (int): Identificador único do voluntário.
        nome (str): Nome do voluntário.
        email (str): Endereço de email do voluntário.
        data (datetime.date): Data do registro de participação do voluntário.

    Methods:
        to_json_Voluntarios(): Converte os dados do voluntário em um dicionário JSON.
    """
    # Define os atributos da tabela Voluntarios
    id = db.Column(db.Integer, primary_key=True)  # Identificador único do voluntário
    nome = db.Column(db.String(100), nullable=False)  # Nome do voluntário
    email = db.Column(db.String(100), nullable=False)  # Endereço de email do voluntário
    data = db.Column(db.Date, nullable=False)  # Data do registro de participação do voluntário
    
    def to_json_Voluntarios(self) -> dict:
        """
        Converte os dados do voluntário para um dicionário JSON.

        Returns:
            dict: Dicionário contendo os dados do voluntário.
        """
        return {'id': self.id, 'name': self.nome, 'email': self.email, 'data': self.data}
