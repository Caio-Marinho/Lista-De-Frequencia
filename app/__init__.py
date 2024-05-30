# Importando as bibliotecas necessárias

from flask import Flask  # Flask é um microframework para Python usado para desenvolver aplicações web.
from app.models import db  # app.models é um módulo que contém as definições dos modelos de banco de dados.
from app.schema import ma  # ma é a instância de Marshmallow, uma biblioteca para serialização/deserialização.
from Menage.menage import migrate, Migracao  # migrate é a instância de Flask-Migrate e Migracao é a função para gerenciar migrações.
from config import Config  # Config é um módulo que contém as configurações do aplicativo.
import mysql.connector  # mysql.connector é um driver de banco de dados que permite a conexão com o MySQL.
from flask_cors import CORS  # flask_cors é uma extensão para lidar com o CORS (Cross-Origin Resource Sharing), permitindo que o seu aplicativo seja acessado por outros domínios.
from flaskenv import arquivo_env # Criar um arquivo env para o ambiente de desenvolvimento aplicando algumas variaveis
import asyncio # Importa a biblioteca asyncio para suporte a programação assíncrona.

asyncio.run(arquivo_env()) # Cria um arquivo env para o ambiente de desenvolvimento aplicando algumas variaveis

def create_database() -> None:  # O '-> None' indica que esta função não retornará nada.
    """
    Função para criar o banco de dados.
    Esta função se conecta ao servidor MySQL e executa uma consulta SQL para criar o banco de dados 'A' se ele não existir.
    """
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='teste',
        port=3306
    )  # Estabelecendo a conexão com o servidor MySQL.
    cursor = conn.cursor()  # Criando um cursor para executar comandos SQL.
    cursor.execute('CREATE DATABASE IF NOT EXISTS FREQUENCIA;')  # Executando o comando para criar o banco de dados.
    cursor.close()  # Fechando o cursor.
    conn.close()  # Fechando a conexão com o servidor MySQL.

def create_app() -> Flask:  # O '-> Flask' indica que esta função retornará uma instância do Flask.
    """
    Função para criar o aplicativo Flask.
    Esta função cria uma instância do aplicativo Flask, habilita o CORS para o aplicativo, carrega as configurações do arquivo config.py, inicializa o banco de dados e registra as rotas.
    """
    
    create_database()  # Chamando a função para criar o banco de dados.
    app = Flask(__name__)  # Criando uma instância do aplicativo Flask.
    CORS(app, resources={r"/*": {"origins": "https://amused-martin-sacred.ngrok-free.app"}})  # Habilitando CORS para o aplicativo.
    app.config.from_object(Config)  # Carregando as configurações do arquivo config.py.
    db.init_app(app)  # Inicializando o banco de dados com a instância do aplicativo Flask.
    ma.init_app(app)  # Inicializando o Marshmallow com a instância do aplicativo Flask.
    migrate.init_app(app,db)  # Inicializando o Flask-Migrate com a instância do aplicativo Flask.
    

    # Criando todas as tabelas no banco de dados quando o aplicativo é executado diretamente.
    with app.app_context():  # Contexto da aplicação para criar as tabelas no banco de dados.
        Migracao()  # Executando a função de migração personalizada.
        db.create_all()  # Criando todas as tabelas definidas nos modelos do banco de dados.
    
    # Importando e registrando as rotas.
    from .routes.routes import bp as routes_bp  # Importando o blueprint de rotas.
    app.register_blueprint(routes_bp)  # Registrando o blueprint de rotas no aplicativo Flask.
    
    return app  # Retornando a instância do aplicativo Flask.
