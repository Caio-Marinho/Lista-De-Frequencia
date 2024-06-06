# ESSA PASTA DEVERIA SE CHAMAR NA VERDADE entities
# Importa os modelos e a instância do banco de dados.
from app.models import db, Calouros, Voluntarios

# Remove acentos de strings.
from unidecode import unidecode

# Importa a classe date para manipulação de datas.
from datetime import date

class Adicionar_Frequencia:
    """
    Classe base para gerenciar frequências, contendo métodos e atributos comuns.
    """
    def __init__(self, nome: str, email: str):
        """
        Inicializa um novo gerenciador de frequência com o nome e email fornecidos.
        
        Args:
            nome (str): O nome da pessoa.
            email (str): O email da pessoa.
        """
        self.__nome = unidecode(nome.strip().title())  # Remove acentos e espaços extras do nome.
        self.__email = email.strip().lower()

    def get_nome(self) -> str:
        """Retorna o nome."""
        return self.__nome

    def get_email(self) -> str:
        """Retorna o email."""
        return self.__email

    def adicionar(self) -> dict:
        """
        Adiciona um registro de frequência. Deve ser implementado pelas subclasses.
        
        Returns:
            dict: Um dicionário contendo o nome da pessoa, email e a contagem de registros associados ao email.
        """
        raise NotImplementedError("Este método deve ser implementado pelas subclasses.")

class Adicionar_Calouro(Adicionar_Frequencia):
    """
    Classe para gerenciar registros de calouros.
    """
    def adicionar(self) -> dict:
        """
        Adiciona um novo registro de calouro ao banco de dados.
        
        Returns:
            dict: Um dicionário contendo o nome do calouro, email e a contagem de registros associados ao email.
        """
        # Cria uma nova instância de Calouros com os dados fornecidos.
        calouro = Calouros(
            nome=self.get_nome(),
            email=self.get_email(),
            data=date.today()  # Define a data atual como data de registro.
        )
        # Adiciona o novo calouro à sessão do banco de dados.
        db.session.add(calouro)
        # Confirma a transação para salvar o registro no banco de dados.
        db.session.commit()
        # Retorna um dicionário com os dados do calouro e a contagem de registros para o email.
        return {
            'student-name': self.get_nome(),
            'email': self.get_email(),
            'count': int(Calouros.query.filter_by(email=self.get_email()).count())
        }

class Adicionar_Voluntario(Adicionar_Frequencia):
    """
    Classe para gerenciar registros de voluntários.
    """
    def adicionar(self) -> dict:
        """
        Adiciona um novo registro de voluntário ao banco de dados.
        
        Returns:
            dict: Um dicionário contendo o nome do voluntário, email e a contagem de registros associados ao email.
        """
        # Cria uma nova instância de Voluntarios com os dados fornecidos.
        voluntario = Voluntarios(
            nome=self.get_nome(),
            email=self.get_email(),
            data=date.today()  # Define a data atual como data de registro.
        )
        # Adiciona o novo voluntário à sessão do banco de dados.
        db.session.add(voluntario)
        # Confirma a transação para salvar o registro no banco de dados.
        db.session.commit()
        # Retorna um dicionário com os dados do voluntário e a contagem de registros para o email.
        return {
            'student-name': self.get_nome(),
            'email': self.get_email(),
            'count': int(Voluntarios.query.filter_by(email=self.get_email()).count())
        }
