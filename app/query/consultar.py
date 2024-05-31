from unidecode import unidecode
from app.schema.schema import DadosSchema_Calouros, DadosSchema_Voluntarios
from app.models.models import Calouros, Voluntarios

class Frequencia:
    def __init__(self, nome:str, email:str, dia:str):
        """
        Inicializa um objeto Frequencia com os atributos nome, email e dia.

        Args:
            nome (str): O nome da pessoa.
            email (str): O endereço de e-mail da pessoa.
            dia (str): A data no formato 'YYYY-MM-DD'.
        """
        self.__nome = unidecode(nome).strip()  # Remove acentos e espaços extras do nome
        self.__email = email
        self.__dia = dia

    def get_nome(self) -> str:
        """Retorna o nome."""
        return self.__nome

    def get_email(self) -> str:
        """Retorna o email."""
        return self.__email

    def get_dia(self) -> str:
        """Retorna o dia."""
        return self.__dia

   
    def consulta_geral(entidade:str='Calouro') -> list:
        """
        Consulta todos os registros da entidade no banco de dados.

        Args:
            entidade (str): O nome da entidade ('Calouro' ou 'Voluntario').

        Returns:
            list: Uma lista contendo todos os registros da entidade.
        """
        # Verifica qual entidade está sendo consultada e realiza a consulta no banco de dados
        if entidade in ('Calouro','calouro','Calouros','calouros'):
            consulta = Calouros.query.all()
        else:
            consulta = Voluntarios.query.all()
        return consulta

    def dicionario_resposta(self, entidade='Calouro') -> dict:
        """
        Retorna um dicionário de resposta para a entidade correspondente.

        Args:
            entidade (str): O nome da entidade ('Calouro' ou 'Voluntario').

        Returns:
            dict: Um dicionário contendo informações sobre o número de registros associados ao email.
        """
        if entidade == 'Calouro':
            return {
                'student-name': self.__nome,
                'email':self.__email,
                'count': int(Calouros.query.filter_by(email=self.__email).count())
            }
        else:
            return {
                'student-name': self.__nome,
                'email':self.__email,
                'count': int(Voluntarios.query.filter_by(email=self.__email).count())
            }

class Calouro(Frequencia):
    def consulta_frequencia(self) -> bool:
        """Consulta a frequência do calouro."""
        consulta = Calouros.query.filter_by(
            nome=self.get_nome(),
            email=self.get_email(),
            data=self.get_dia()
        ).all()
        dados = DadosSchema_Calouros(many=True).dumps(consulta, indent=2)
        print(dados)
        print(self.get_dia())
        return self.get_dia() in dados

class Voluntario(Frequencia):
    def consulta_frequencia(self) -> bool:
        """Consulta a frequência do voluntário."""
        consulta = Voluntarios.query.filter_by(
            nome=self.get_nome(),
            email=self.get_email(),
            data=self.get_dia()
        ).all()
        dados = DadosSchema_Voluntarios(many=True).dumps(consulta, indent=2)
        print(dados)
        print(self.get_dia())
        return self.get_dia() in dados
