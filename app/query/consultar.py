# Importa a função unidecode do módulo unidecode para remover acentos de strings.
from unidecode import unidecode
# Importa os esquemas de dados DadosSchema_Calouros e DadosSchema_Voluntarios do módulo schema do pacote app.
from app.schema.schema import DadosSchema_Calouros, DadosSchema_Voluntarios
# Importa os modelos Calouros e Voluntarios do módulo models do pacote app.
from app.models.models import Calouros, Voluntarios

class Frequencia:
    """
    Classe base para consultar a frequência de calouros e voluntários.
    """
    def __init__(self, nome: str, email: str, dia: str):
        """
        Inicializa um objeto Frequencia com os atributos nome, email e dia.

        Args:
            nome (str): O nome da pessoa.
            email (str): O endereço de e-mail da pessoa.
            dia (str): A data no formato 'YYYY-MM-DD'.
        """
        self.__nome = unidecode(nome.strip().title())  # Remove acentos e espaços extras do nome
        self.__email = str(email).strip()
        self.__dia = dia

    # Métodos get para acessar os atributos privados nome, email e dia.
    def get_nome(self):
        return self.__nome
    
    def get_email(self):
        return self.__email
    
    def get_dia(self):
        return self.__dia
   
    def consulta_geral(entidade: str) -> list:
        """
        Consulta todos os registros da entidade no banco de dados.

        Args:
            entidade (str): O nome da entidade ('Calouro' ou 'Voluntario').

        Returns:
            list: Uma lista contendo todos os registros da entidade.
        """
        # Verifica qual entidade está sendo consultada e realiza a consulta no banco de dados
        if entidade is None:
            pass
        else:
            if entidade in ('Calouro', 'calouro', 'Calouros', 'calouros'):
                consulta = Calouros.query.all()
            elif entidade in ('Voluntario', 'Voluntarios', 'voluntario', 'voluntarios'):
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
        # Verifica a entidade e retorna um dicionário com as informações do nome, email e contagem de registros.
        if entidade == 'Calouro':
            return {
                'student-name': self.__nome,
                'email': self.__email,
                'count': int(Calouros.query.filter_by(nome=self.__nome, email=self.__email).count())
            }
        else:
            return {
                'student-name': self.__nome,
                'email': self.__email,
                'count': int(Voluntarios.query.filter_by(nome=self.__nome, email=self.__email).count())
            }

class Calouro(Frequencia):
    """
    Classe para consultar a frequência de calouros.
    """
    def consulta_frequencia(self) -> bool:
        """Consulta a frequência do calouro."""
        consultaCompletaDia = Calouros.query.filter_by(
            nome=self.get_nome(),
            email=self.get_email(),
            data=self.get_dia()
        ).all()
        
        dadosCompletoDia = DadosSchema_Calouros(many=True).dumps(consultaCompletaDia, indent=2)
        
        consultaCompleto = Calouros.query.filter_by(
            nome=self.get_nome(),
            email=self.get_email(),
        ).all()
        
        dadosCompleto = DadosSchema_Calouros(many=True).dumps(consultaCompleto, indent=2)
        
        consultaNome = Calouros.query.filter_by(
            nome=self.get_nome(),
        ).all()
        
        dadosNome = DadosSchema_Calouros(many=True).dumps(consultaNome, indent=2)
        
        consultaEmail = Calouros.query.filter_by(
            email=self.get_email(),
        ).all()
        
        dadosEmail = DadosSchema_Calouros(many=True).dumps(consultaEmail, indent=2)
        
        email_DadosCompleto = self.get_email() in dadosCompletoDia
        
        email_DadosEmail = self.get_email() in dadosEmail
        
        nome_dadosCompleto = self.get_nome() in dadosCompletoDia
        
        RegistradaPresenca = self.get_dia() in dadosCompletoDia
        
        nome_dadosNome = self.get_nome() in dadosNome
        
        Completo = all([self.get_nome() in dadosCompleto,self.get_email() in dadosCompleto])
        
        verdade = [Completo==email_DadosEmail,Completo==nome_dadosNome,not all([nome_dadosCompleto,email_DadosCompleto])]
        
        if len(dadosEmail)==0 and len(dadosNome)==0:
            return True, RegistradaPresenca
        elif all(verdade):
            return all(verdade), RegistradaPresenca

class Voluntario(Frequencia):
    """
    Classe para consultar a frequência de voluntários.
    """
    def consulta_frequencia(self) -> bool:
        """Consulta a frequência do calouro."""
        consultaCompletaDia = Voluntarios.query.filter_by(
            nome=self.get_nome(),
            email=self.get_email(),
            data=self.get_dia()
        ).all()
        
        dadosCompletoDia = DadosSchema_Voluntarios(many=True).dumps(consultaCompletaDia, indent=2)
        
        consultaCompleta = Voluntarios.query.filter_by(
            nome=self.get_nome(),
            email=self.get_email(),
        ).all()
        
        dadosCompleto = DadosSchema_Voluntarios(many=True).dumps(consultaCompleta, indent=2)
        
        consultaNome = Voluntarios.query.filter_by(
            nome=self.get_nome(),
            data=self.get_dia()
        ).all()
        
        dadosNome = DadosSchema_Voluntarios(many=True).dumps(consultaNome, indent=2)
       
        consultaEmail = Voluntarios.query.filter_by(
            email=self.get_email(),
            data=self.get_dia()
        ).all()
        
        dadosEmail = DadosSchema_Voluntarios(many=True).dumps(consultaEmail, indent=2)
        
        email_DadosCompleto = self.get_email() in dadosCompletoDia
        
        email_DadosEmail = self.get_email() in dadosEmail
        
        nome_dadosCompleto = self.get_nome() in dadosCompletoDia
        
        nome_dadosNome = self.get_nome() in dadosNome
        
        completo = all([self.get_nome() in dadosCompleto,self.get_email() in dadosCompleto])
        
        verdade = [completo==email_DadosEmail,completo==nome_dadosNome,not all([email_DadosCompleto, nome_dadosCompleto])]
        
        if len(dadosEmail)==0 and len(dadosNome)==0:
            return True,self.get_dia() in dadosCompletoDia
        else:
            return all(verdade), self.get_dia() in dadosCompletoDia
