import os # Os fornece uma maneira de usar funcionalidades dependentes do sistema operacional, como verificar se um diretório existe.
from flask_migrate import init # Migrate é a classe para gerenciar migrações e init é a função para inicializar as migrações.
from app.models import db

from . import migrate

migrate

def Migracao() -> None:  # O '-> None' indica que esta função não retornará nada.
    """
    Função para inicializar o diretório de migrações.
    Esta função verifica se o diretório 'migrations' existe e, caso não exista, inicializa as migrações.
    """
    if not os.path.exists('migrations'):  # Verificando se o diretório 'migrations' não existe.
        init()  # Inicializando as migrações.