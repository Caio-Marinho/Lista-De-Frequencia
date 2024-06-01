# Importa a extensão SQLAlchemy para interagir com o banco de dados
from flask_sqlalchemy import SQLAlchemy

# Cria uma instância de SQLAlchemy para ser usada em todo o aplicativo Flask.
# Essa instância é responsável por representar o banco de dados e executar operações relacionadas a ele.
db = SQLAlchemy()


# Importa os modelos de banco de dados do diretório 'models'.
# Os modelos definem a estrutura das tabelas do banco de dados e fornecem métodos para manipular os dados nelas contidos,
# como inserir, consultar, atualizar e excluir registros.
from .models import Calouros, Voluntarios

# Importa outras classes de modelo de banco de dados do diretório 'models', se necessário.
# Este padrão de importação é útil para organizar o código em módulos e pacotes, permitindo que você importe as definições
# de classe de modelo de outros arquivos dentro do diretório 'models' usando 'from .models import OutraClasse'.
# A importação de outros modelos de Banco de dados podendo ser passado
# from [diretorio].[Arquivo] ou .[Arquivo] ou [Arquivo] import [Classe]
