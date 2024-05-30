import os


class Config:
    """Configuração básica para a aplicação."""

    # Configurações básicas

    # A chave secreta é usada para proteger sessões e cookies gerados pelo Flask.
    # A chave secreta deve ser mantida em segredo e nunca deve ser compartilhada publicamente.
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(24).hex())

    # Define se o modo de depuração está ativado.
    # O modo de depuração deve ser desativado em produção para evitar vazamentos de informações sensíveis.
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG', True)  # Use variáveis de ambiente para controlar o modo de depuração.

    # Configurações do banco de dados

    # Define a URI do banco de dados para MySQL.
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI',
                                             'mysql+mysqlconnector://username:password@hostname:port/database')
    """
    
    URI de conexão para um banco de dados MySQL.

    Formato da URI:
        mysql+mysqlconnector://<usuário>:<senha>@<host>:<porta>/<nome_do_banco>

    Exemplo:
        mysql+mysqlconnector://username:password@hostname:port/database
    """

    # Define a URI do banco de dados para PostgresSQL.
    """SQLALCHEMY_DATABASE_URI_POSTGRES = os.environ.get('SQLALCHEMY_DATABASE_URI_POSTGRES', 
    'postgresql://postgres:teste@localhost/frequencia')

    URI de conexão para um banco de dados PostgresSQL.

    Formato da URI:
        postgresql://<usuário>:<senha>@<host>:<porta>/<nome_do_banco>

    Exemplo:
        postgresql://postgres:password@hostname:port/database
    """

    # Define a URI do banco de dados para MariaDB.
    """SQLALCHEMY_DATABASE_URI_MARIADB = os.environ.get('SQLALCHEMY_DATABASE_URI_MARIADB', 
    'mysql+mysqlconnector://root:teste@localhost/frequencia')
    
    URI de conexão para um banco de dados MariaDB.

    Formato da URI:
        mysql+mysqlconnector://<usuário>:<senha>@<host>:<porta>/<nome_do_banco>

    Exemplo:
        mysql+mysqlconnector://username:password@hostname:port/database
    """

    # Define a URI do banco de dados para SQLite.

    """
    SQLALCHEMY_DATABASE_URI_SQLITE = os.environ.get('SQLALCHEMY_DATABASE_URI_SQLITE', 'sqlite:///path/to/database.db')
    
    URI de conexão para um banco de dados SQLite.

    Formato da URI:
        sqlite:///caminho/para/o/arquivo.db

    Exemplo:
        sqlite:///path/to/database.db
    """

    # Define a URI do banco de dados para Oracle.
    """SQLALCHEMY_DATABASE_URI_ORACLE = os.environ.get('SQLALCHEMY_DATABASE_URI_ORACLE', 
    'oracle://username:password@hostname:port/sid')
    
    URI de conexão para um banco de dados Oracle.

    Formato da URI:
        oracle://<usuário>:<senha>@<host>:<porta>/<SID>

    Exemplo:
        oracle://username:password@hostname:port/sid
    """

    # Define a URI do banco de dados para Microsoft SQL Server.
    """SQLALCHEMY_DATABASE_URI_MSSQL = os.environ.get('SQLALCHEMY_DATABASE_URI_MSSQL', 
    'mssql+pyodbc://username:password@hostname:port/database?driver=ODBC+Driver+17+for+SQL+Server')
    
    URI de conexão para um banco de dados Microsoft SQL Server.

    Formato da URI:
        mssql+pyodbc://<usuário>:<senha>@<host>:<porta>/<nome_do_banco>?driver=<driver>

    Exemplo:
        mssql+pyodbc://username:password@hostname:port/database?driver=ODBC+Driver+17+for+SQL+Server
    """

    # Define se as modificações no banco de dados devem ser rastreadas. Isso ajuda no controle de versão do banco de
    # dados.
    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS',
                                                    True)  # Desative para evitar avisos de desempenho.

    # Define se os modelos devem ser recarregados automaticamente sempre que forem modificados.
    # Isso é útil durante o desenvolvimento, mas deve ser desativado em produção para melhorar o desempenho.
    TEMPLATES_AUTO_RELOAD = os.environ.get('TEMPLATES_AUTO_RELOAD', True)
