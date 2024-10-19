# Importando a biblioteca Flask-Marshmallow
# Flask-Marshmallow é uma extensão leve para Flask que adiciona suporte simplificado para 
# serialização de objetos complexos para tipos de dados Python nativos.
from flask_marshmallow import Marshmallow

# Inicializando o objeto Marshmallow
# Aqui, estamos criando uma instância do Marshmallow. Esta instância será usada para criar 
# esquemas para serialização/desserialização. A serialização é o processo de transformar 
# dados complexos em formatos mais simples para armazenamento ou transmissão, e a desserialização 
# é o processo inverso.
ma = Marshmallow()

# Importando o esquema DadosSchema_Calouros do módulo schema
# Um esquema em Marshmallow é uma maneira de representar a estrutura dos dados que queremos 
# serializar/desserializar. Aqui, estamos importando o esquema DadosSchema_Calouros, que 
# define a estrutura dos dados para os calouros.
from .schema import DadosSchema_Calouros, DadosSchema_Voluntarios
