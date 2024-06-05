from flask import Flask  # Importa a classe Flask do pacote Flask.
from app.models import db  # Importa o banco de dados definido no módulo models.
from app.schema import ma  # Importa o Marshmallow para serialização/deserialização.
from Menage.menage import migrate, Migracao  # Importa o Flask-Migrate para migração de banco de dados.
from app.Config.config import Config  # Importa as configurações do aplicativo do módulo config.
from flask_cors import CORS  # Importa o Flask-CORS para lidar com o CORS.
from flaskenv import arquivo_env  # Importa a função para criar um arquivo env para o ambiente de desenvolvimento.
import asyncio  # Importa a biblioteca asyncio para suporte a programação assíncrona.


asyncio.run(arquivo_env())  # Cria um arquivo env para o ambiente de desenvolvimento aplicando algumas variáveis.


def create_app() -> Flask:
    """
    Função para criar o aplicativo Flask.
    
    Esta função cria uma instância do aplicativo Flask, habilita o CORS para o aplicativo, carrega as configurações do arquivo config.py, inicializa o banco de dados e registra as rotas.
    
    Returns:
        Flask: A instância do aplicativo Flask.
    """
    Config.create_database()  # Chama a função para criar o banco de dados.

    app = Flask(__name__)  # Cria uma instância do aplicativo Flask.
    
    # Habilita o CORS para o aplicativo, permitindo acesso de outros domínios.
    CORS(app, resources={r"/*": {"origins": "https://amused-martin-sacred.ngrok-free.app"}})
    
    app.config.from_object(Config)  # Carrega as configurações do arquivo config.py.
    
    db.init_app(app)  # Inicializa o banco de dados com a instância do aplicativo Flask.
    ma.init_app(app)  # Inicializa o Marshmallow com a instância do aplicativo Flask.
    migrate.init_app(app,db)  # Inicializa o Flask-Migrate com a instância do aplicativo Flask.

    # Cria todas as tabelas no banco de dados quando o aplicativo é executado diretamente.
    with app.app_context():  # Cria um contexto de aplicação para criar as tabelas no banco de dados.
        Migracao()  # Executa a função de migração personalizada.
        db.create_all()  # Cria todas as tabelas definidas nos modelos do banco de dados.
    
    # Importa e registra as rotas.
    from .routes.routes import bp as routes_bp  # Importa o blueprint de rotas.
    app.register_blueprint(routes_bp)  # Registra o blueprint de rotas no aplicativo Flask.
    
    return app  # Retorna a instância do aplicativo Flask.
