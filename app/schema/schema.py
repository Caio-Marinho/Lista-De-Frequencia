from . import ma
from app.models import Calouros, Voluntarios

class DadosSchema_Calouros(ma.SQLAlchemySchema):
    """
    A classe DadosSchema_Calouros é um esquema Marshmallow que representa a estrutura de dados do modelo Calouros.
    Este esquema é usado para serializar e desserializar instâncias do modelo Calouros, permitindo a conversão fácil entre objetos Python e JSON.
    """
    class Meta:
        model: type = Calouros  # O modelo que este esquema irá serializar/desserializar.

    id = ma.auto_field()  # Campo 'id' do modelo 'Calouros'.
    nome = ma.auto_field()   # Campo 'nome' do modelo 'Calouros'.
    email = ma.auto_field()  # Campo 'email' do modelo 'Calouros'.

class DadosSchema_Voluntarios(ma.SQLAlchemyAutoSchema):
    """
    A classe DadosSchema_Voluntarios é um esquema Marshmallow que representa a estrutura de dados do modelo Voluntarios.
    Este esquema é usado para serializar e desserializar instâncias do modelo Voluntarios, permitindo a conversão fácil entre objetos Python e JSON.
    """
    class Meta:
        model: type = Voluntarios  # O modelo que este esquema irá serializar/desserializar.
